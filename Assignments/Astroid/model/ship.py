import math
import pygame as pg

import config
from model.bullet import Bullet
from model.forcefield import Forcefield
from model.ship_type import ShipType

class Ship:
    '''Model for Asteroid ship.'''
    def __init__(self, ship_type: int):
        self.ship_type = ship_type
        self.alive = True
        self.x = config.SHIP_X
        self.y = config.SHIP_Y
        self.radius = 34
        self.angle = 0
        self.vx = 0.0
        self.vy = 0.0

        self.forcefield = Forcefield(self.x, self.y)

        self.bullets = []
        self.time_last_bullet = 0

        self.sound_bullet = pg.mixer.Sound('assets/bullet.wav')

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.vx != 0 or self.vy != 0:
            # Apply drag
            self.vx *= config.DRAG ** dt
            self.vy *= config.DRAG ** dt
            
            # Limit the MAX SPEED
            current_speed = math.hypot(self.vx, self.vy)
            
            if current_speed > config.MAX_SPEED:
                # Calculate the necessary scale factor to bring speed back to MAX_SPEED
                scale_factor = config.MAX_SPEED / current_speed
                self.vx *= scale_factor
                self.vy *= scale_factor

        if self.x > config.HARD_BOUNDARY_RIGHT:
            self.x = config.HARD_BOUNDARY_LEFT
        elif self.x < config.HARD_BOUNDARY_LEFT:
            self.x = config.HARD_BOUNDARY_RIGHT
        elif self.y > config.HARD_BOUNDARY_BOTTOM:
            self.y = config.HARD_BOUNDARY_TOP
        elif self.y < config.HARD_BOUNDARY_TOP:
            self.y = config.HARD_BOUNDARY_BOTTOM

        # Update the forcefield position and animation
        self.forcefield.recenter(self.x, self.y)
        self.forcefield.update() # Call the update for the glow animation

        # Bullets
        for i in self.bullets:
            i.update(dt)
        self.bullets = [bullet for bullet in self.bullets if not bullet.expired]

    def rotate(self, dt, direction):
        '''Rotate ship.'''
        self.angle += direction * config.ROTATION_SPEED * dt
        self.angle %= 360 # Keep angle in [0, 360)

    def thrust(self, dt):
        '''Apply forward thrust in the direction the ship is facing.'''
        rad = math.radians(self.angle-90)
        self.vx += math.cos(rad) * config.THRUST_POWER * dt
        self.vy += math.sin(rad) * config.THRUST_POWER * dt

    def brake(self, dt):
        """Apply braking force to slow down the ship."""
        speed = math.hypot(self.vx, self.vy)
        if speed == 0:
            return

        # Braking deceleration power
        brake_power = config.BRAKE_POWER * dt

        # Compute scaling factor so we don't reverse direction
        scale = max((speed - brake_power) / speed, 0)

        self.vx *= scale
        self.vy *= scale


    def fire_bullet(self):
        time_current = pg.time.get_ticks()

        current_time = pg.time.get_ticks()
        
        # Check if enough time has passed since the last shot
        if current_time - self.time_last_bullet > config.FIRE_DELAY_MS:
            
            # Fire the bullet
            self.bullets.append(Bullet(self.x, self.y, self.angle))
            pg.mixer.Sound.play(self.sound_bullet)
            
            # Reset the timer
            self.time_last_bullet = current_time
