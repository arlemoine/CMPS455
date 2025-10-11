from paddle import Paddle
from ball import Ball
from bullet import Bullet
from particle import Particle
import random
import pygame as pg


class PongModel:
    """Model for Pong With Guns."""

    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height

        BOUNDARY_TOP = 0
        BOUNDARY_BOTTOM = self.height       
        BOUNDARY_LEFT = 0
        BOUNDARY_RIGHT = self.width 

        self.paddle1 = Paddle(50, self.height // 2, BOUNDARY_TOP, BOUNDARY_BOTTOM)
        self.paddle2 = Paddle(self.width - 60, self.height // 2, BOUNDARY_TOP, BOUNDARY_BOTTOM)
        self.paddles = [self.paddle1, self.paddle2]

        self.ball = Ball(self.width // 2, self.height // 2, BOUNDARY_TOP, BOUNDARY_BOTTOM, BOUNDARY_LEFT, BOUNDARY_RIGHT)
        self.balls = [self.ball]

        self.bullets = []
        self.particles = []

        # Fire rate (seconds)
        self.SHOOT_RATE = 1
        self.last_shot_time_p1 = 0
        self.last_shot_time_p2 = 0

        # Heat system
        self.MAX_HEAT = 100
        self.HEAT_PER_SHOT = 12
        self.HEAT_COOLDOWN_RATE = 40    # per second
        self.OVERHEAT_COOLDOWN_RATE = 20  # per second
        self.p1_heat = 0
        self.p2_heat = 0
        self.p1_overheated = False
        self.p2_overheated = False

        self.MAX_BOUNCE_SPEED_Y = 300
        self.MAX_BOUNCE_ANGLE = 75

        self.ROUND_DELAY = 1.5  # seconds
        self.round_timer = self.ROUND_DELAY
        self.next_direction_x = random.choice([-1, 1]) 

        pg.mixer.init()
        self.sound_bounce = pg.mixer.Sound('assets/bounce.mp3')
        self.sound_hit = pg.mixer.Sound('assets/hit.mp3')
        self.sound_bullet = pg.mixer.Sound('assets/bullet.mp3')

    def update(self, dt):
        if self.round_timer > 0:
            self.round_timer -= dt
            if self.round_timer <= 0:
                self.ball.vx = self.MAX_BOUNCE_SPEED_Y * self.next_direction_x
                self.ball.vy = self.MAX_BOUNCE_SPEED_Y * 0.5 * random.uniform(0.2, 1.0) * random.choice([-1, 1])

        if self.round_timer <= 0:
            self.collision_check()
            self.bullet_collision_check()
            self.update_ai_paddle()

            self.paddle1.update_size(dt)
            self.paddle2.update_size(dt)

            for paddle in self.paddles:
                paddle.move(dt)
            for ball in self.balls:
                ball.move(dt)

            self.bullets = [b for b in self.bullets if b.move(dt)]
            self.particles = [p for p in self.particles if p.update(dt)]

            self.check_score()
            self.cool_guns(dt)

    def collision_check(self):
        ball = self.ball

        # Paddle 1
        if ball.hitbox_x2 >= self.paddle1.hitbox_x1 and ball.hitbox_x1 <= self.paddle1.hitbox_x2 \
           and ball.hitbox_y2 >= self.paddle1.hitbox_y1 and ball.hitbox_y1 <= self.paddle1.hitbox_y2:
            rel_y = ball.y - self.paddle1.y
            ball.vy = (rel_y / (self.paddle1.height / 2)) * self.MAX_BOUNCE_SPEED_Y
            ball.vx = abs(ball.vx) * 1.05
            pg.mixer.Sound.play(self.sound_bounce)
            return True

        # Paddle 2
        elif ball.hitbox_x2 >= self.paddle2.hitbox_x1 and ball.hitbox_x1 <= self.paddle2.hitbox_x2 \
             and ball.hitbox_y2 >= self.paddle2.hitbox_y1 and ball.hitbox_y1 <= self.paddle2.hitbox_y2:
            rel_y = ball.y - self.paddle2.y
            ball.vy = (rel_y / (self.paddle2.height / 2)) * self.MAX_BOUNCE_SPEED_Y
            ball.vx = -abs(ball.vx) * 1.05
            pg.mixer.Sound.play(self.sound_bounce)
            return True

        return False

    def bullet_collision_check(self):
        BALL_SPEED_INCREMENT_FACTOR = 0.3
        active_bullets = []

        for bullet in self.bullets:
            hit = False
            if bullet.hitbox_x2 >= self.ball.hitbox_x1 and bullet.hitbox_x1 <= self.ball.hitbox_x2 \
               and bullet.hitbox_y2 >= self.ball.hitbox_y1 and bullet.hitbox_y1 <= self.ball.hitbox_y2:
                self.ball.vx += bullet.vx * BALL_SPEED_INCREMENT_FACTOR
                self.particles.append(Particle(bullet.x, bullet.y))
                pg.mixer.Sound.play(self.sound_hit)
                hit = True

            elif bullet.vx > 0 and bullet.hitbox_x2 >= self.paddle2.hitbox_x1 and bullet.hitbox_x1 <= self.paddle2.hitbox_x2 \
                 and bullet.hitbox_y2 >= self.paddle2.hitbox_y1 and bullet.hitbox_y1 <= self.paddle2.hitbox_y2:
                self.paddle2.shrink_on_hit()
                self.particles.append(Particle(bullet.x, bullet.y))
                pg.mixer.Sound.play(self.sound_hit)
                hit = True

            elif bullet.vx < 0 and bullet.hitbox_x2 >= self.paddle1.hitbox_x1 and bullet.hitbox_x1 <= self.paddle1.hitbox_x2 \
                 and bullet.hitbox_y2 >= self.paddle1.hitbox_y1 and bullet.hitbox_y1 <= self.paddle1.hitbox_y2:
                self.paddle1.shrink_on_hit()
                self.particles.append(Particle(bullet.x, bullet.y))
                pg.mixer.Sound.play(self.sound_hit)
                hit = True

            if not hit:
                active_bullets.append(bullet)

        self.bullets = active_bullets

    def update_ai_paddle(self):
        target_y = self.ball.y if self.ball.x > self.width // 2 else self.paddle1.y
        TOLERANCE = 10
        if self.paddle2.y < target_y - TOLERANCE:
            self.paddle2.set_direction(1)
        elif self.paddle2.y > target_y + TOLERANCE:
            self.paddle2.set_direction(-1)
        else:
            self.paddle2.set_direction(0)

    def check_score(self):
        if self.ball.x < 0:
            return 2
        elif self.ball.x > self.width:
            return 1
        return 0

    def reset_ball(self, direction_x):
        self.ball.x = self.width // 2
        self.ball.y = self.height // 2
        center_y = self.height // 2
        for paddle in [self.paddle1, self.paddle2]:
            paddle.y = center_y
            paddle.height = paddle.original_height
            paddle.speed = paddle.base_speed
            paddle.update_hitbox()

        self.p1_heat = self.p2_heat = 0
        self.p1_overheated = self.p2_overheated = False

        self.round_timer = self.ROUND_DELAY
        self.ball.vx = self.ball.vy = 0
        self.next_direction_x = direction_x
        self.bullets = []
        self.particles = []

    def fire_bullet(self, player_id, current_time):
        if player_id == 1:
            last_shot, heat, overheated = self.last_shot_time_p1, self.p1_heat, self.p1_overheated
        else:
            last_shot, heat, overheated = self.last_shot_time_p2, self.p2_heat, self.p2_overheated

        if current_time - last_shot < self.SHOOT_RATE or overheated:
            return False
        if heat >= self.MAX_HEAT:
            if player_id == 1:
                self.p1_overheated = True
            else:
                self.p2_overheated = True
            return False

        paddle = self.paddle1 if player_id == 1 else self.paddle2
        direction = 1 if player_id == 1 else -1
        offset = paddle.width // 2 + 5
        new_bullet = Bullet(paddle.x + offset * direction, paddle.y, direction, 0, self.height, 0, self.width)
        self.bullets.append(new_bullet)

        if player_id == 1:
            self.last_shot_time_p1 = current_time
            self.p1_heat += self.HEAT_PER_SHOT
        else:
            self.last_shot_time_p2 = current_time
            self.p2_heat += self.HEAT_PER_SHOT

        pg.mixer.Sound.play(self.sound_bullet)
        return True

    def cool_guns(self, dt):
        self.p1_heat = max(0, self.p1_heat - (self.OVERHEAT_COOLDOWN_RATE if self.p1_overheated else self.HEAT_COOLDOWN_RATE) * dt)
        self.p1_overheated = self.p1_overheated and self.p1_heat > 0

        self.p2_heat = max(0, self.p2_heat - (self.OVERHEAT_COOLDOWN_RATE if self.p2_overheated else self.HEAT_COOLDOWN_RATE) * dt)
        self.p2_overheated = self.p2_overheated and self.p2_heat > 0

    def update_ai_shooting(self, current_time):
        if self.ball.x < self.width // 2 and self.ball.vx < 0:
            self.fire_bullet(2, current_time)
