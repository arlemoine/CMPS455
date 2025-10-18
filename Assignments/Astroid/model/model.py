import config
import random
import pygame as pg
from model.ship import Ship
from model.particle import Particle

class Model:
    """Model for Pong With Guns."""

    def __init__(self, ship_type):
        self.ship = Ship(ship_type)
        self.asteroids = []
        self.explosions = []
        self.particles = []
        self.last_particle_spawn_time = 0

        # pg.mixer.init()
        # self.sound_bounce = pg.mixer.Sound('assets/bounce.mp3')
        # self.sound_hit = pg.mixer.Sound('assets/hit.mp3')
        # self.sound_bullet = pg.mixer.Sound('assets/bullet.mp3')

    def update(self, dt):
        # Ship
        self.ship.update(dt)  

    def menu_update(self, dt):
        current_time = pg.time.get_ticks()

        self.particles = [p for p in self.particles if (p.update(dt) or not p.expired)]

        random_delay = config.PARTICLE_GENERATION * random.uniform(0.8, 1.5)
        if current_time - self.last_particle_spawn_time > random_delay:
            self.particles.append(Particle())
            self.last_particle_spawn_time = current_time    
