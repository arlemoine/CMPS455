import config
import math
import random
import pygame as pg
from model.ship import Ship
from model.astroid import Astroid
from model.explosion import Explosion
from model.particle import Particle

class Model:
    """Main model for Astroids."""

    def __init__(self, ship_type):
        self.ship = Ship(ship_type)
        self.gameOver = False
        self.score = 0
        self.astroids = []
        self.explosions = []
        self.particles = []
        self.last_astroid_spawn_time = 0
        self.last_particle_spawn_time = 0

        self.astroid_spawn_rate = config.ASTROID_SPAWN_RATE_START
        self.total_time = 0
        self.level = 1 # Starting difficulty level

        # pg.mixer.init()
        # self.sound_bounce = pg.mixer.Sound('assets/bounce.mp3')
        # self.sound_hit = pg.mixer.Sound('assets/hit.mp3')
        # self.sound_bullet = pg.mixer.Sound('assets/bullet.mp3')

    def update(self, dt):
        """Update the game state."""
        if self.ship.alive:
            self.ship.update(dt)

        new_astroids = []
        astroids_to_remove = set()
        explosions_to_add = []

        # 1️⃣ Update asteroids
        for astroid in self.astroids:
            if astroid.update(dt):
                new_astroids.append(astroid)
        self.astroids = new_astroids

        # 2️⃣ Check collisions

        # Check asteroid-to-asteroid collisions
        for i in range(len(self.astroids)):
            a1 = self.astroids[i]
            for j in range(i + 1, len(self.astroids)):
                a2 = self.astroids[j]
                dx = a2.x - a1.x
                dy = a2.y - a1.y
                distance = math.hypot(dx, dy)
                if distance < a1.radius + a2.radius:
                    # Resolve overlap
                    overlap = (a1.radius + a2.radius - distance) / 2
                    if distance != 0:
                        nx = dx / distance
                        ny = dy / distance
                        a1.x -= nx * overlap
                        a1.y -= ny * overlap
                        a2.x += nx * overlap
                        a2.y += ny * overlap

                    # Update velocities
                    a1.bounce_off(a2)
                    
        # Track bullets that hit
        bullets_to_remove = []

        for astroid in self.astroids:
            # Bullet collisions
            for bullet in self.ship.bullets:
                if self.collision_check(bullet, astroid):
                    astroid.size -= 1
                    astroid.calc_radius()
                    self.score += 1
                    bullets_to_remove.append(bullet)

                    if astroid.size <= 0:
                        astroids_to_remove.add(astroid)
                        self.score += 3
                        explosions_to_add.append(Explosion(astroid.x, astroid.y))
                    break  # One bullet hits only one asteroid

            # Forcefield / ship collisions
            if self.ship.forcefield.health > 0:
                if self.collision_check(self.ship.forcefield, astroid):
                    if self.ship.forcefield.damage():  # returns True if destroyed?
                        astroids_to_remove.add(astroid)
            else:
                if self.collision_check(self.ship, astroid):
                    # Ship collides — create explosion immediately
                    explosions_to_add.append(Explosion(self.ship.x, self.ship.y))
                    self.ship.alive = False
                    self.gameOver = True
                    astroids_to_remove.add(astroid)  # optional: remove asteroid too

        # 3️⃣ Remove bullets that hit
        self.ship.bullets = [b for b in self.ship.bullets if b not in bullets_to_remove]

        # 4️⃣ Remove asteroids that were destroyed
        self.astroids = [a for a in self.astroids if a not in astroids_to_remove]

        # 5️⃣ Add new explosions
        self.explosions.extend(explosions_to_add)

        # 6️⃣ Update explosions
        for explosion in self.explosions[:]:
            explosion.update(dt)
            if not explosion.alive:
                self.explosions.remove(explosion)

        # 7️⃣ Random asteroid spawning
        current_time = pg.time.get_ticks()
        self.total_time += dt  # dt is in seconds

        # Adjust spawn rate over time
        self.astroid_spawn_rate = max(
            config.ASTROID_SPAWN_RATE_MIN,
            config.ASTROID_SPAWN_RATE_START - config.ASTROID_SPAWN_ACCEL * self.total_time * 1000
        )

        # Level 1 = start, level 10 = near fastest spawn rate
        spawn_range = config.ASTROID_SPAWN_RATE_START - config.ASTROID_SPAWN_RATE_MIN
        if spawn_range > 0:
            self.level = int(
                1 + 9 * (config.ASTROID_SPAWN_RATE_START - self.astroid_spawn_rate) / spawn_range
            )
        else:
            self.level = 1

        # Randomized delay to avoid too uniform spawns
        random_delay = self.astroid_spawn_rate * random.uniform(0.8, 1.2)
        if current_time - self.last_astroid_spawn_time > random_delay:
            self.generate_astroid()
            self.last_astroid_spawn_time = current_time

        # 8️⃣ Return -1 if game over
        if self.gameOver:
            return -1


    def menu_update(self, dt):
        current_time = pg.time.get_ticks()

        self.particles = [p for p in self.particles if (p.update(dt) or not p.expired)]

        random_delay = config.PARTICLE_GENERATION * random.uniform(0.8, 1.5)
        if current_time - self.last_particle_spawn_time > random_delay:
            self.particles.append(Particle())
            self.last_particle_spawn_time = current_time   

    def generate_astroid(self):
        edge = random.randrange(1, 5)

        if edge == 1:
            y = config.HARD_BOUNDARY_TOP + (abs(0 - config.HARD_BOUNDARY_TOP) // 2)
            x = random.randrange(config.HARD_BOUNDARY_LEFT, config.HARD_BOUNDARY_RIGHT)
        elif edge == 2:
            x = config.HARD_BOUNDARY_RIGHT - (abs(config.SOFT_BOUNDARY_RIGHT - config.HARD_BOUNDARY_RIGHT) // 2)
            y = random.randrange(config.HARD_BOUNDARY_TOP, config.HARD_BOUNDARY_BOTTOM)
        elif edge == 3:
            y = config.HARD_BOUNDARY_BOTTOM - (abs(config.SOFT_BOUNDARY_BOTTOM - config.HARD_BOUNDARY_BOTTOM) // 2)
            x = random.randrange(config.HARD_BOUNDARY_LEFT, config.HARD_BOUNDARY_RIGHT)
        elif edge == 4:
            x = config.HARD_BOUNDARY_LEFT + (abs(config.SOFT_BOUNDARY_LEFT - config.HARD_BOUNDARY_LEFT) // 2)
            y = random.randrange(config.HARD_BOUNDARY_TOP, config.HARD_BOUNDARY_BOTTOM)

        self.astroids.append(Astroid(x, y))

    def collision_check(self, object1, object2):
        dx = object1.x - object2.x
        dy = object1.y - object2.y
        distance_sq = dx*dx + dy*dy
        radius_sum = object1.radius + object2.radius
        return distance_sq <= radius_sum * radius_sum