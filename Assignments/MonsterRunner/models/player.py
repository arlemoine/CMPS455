import pygame as pg
from pygame.math import Vector2 as vec
import config
from enum import Enum

GRAVITY = vec(0, 1000)
DECELERATION = vec(0.8, 0)
player_width, player_height = 100, 100

class PlayerState(Enum):
    RUN = 0
    JUMP = 1
    SLIDE = 2

class Player:
    def __init__(self):
        self.width, self.height = player_width, player_height
        self.state = PlayerState.RUN
        self.pos = vec(200, config.GROUND_HEIGHT - self.height)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.max_vel = vec(100, 0)
        self.on_ground = True
        self.jump_force = vec(0, -600)
        self.slide_time = 3000 # milliseconds
        self.time_since_slide = 0
        self.colliding = False

    def jump(self):
        if self.on_ground:
            self.state = PlayerState.JUMP
            self.width, self.height = 100, 80
            self.on_ground = False
            self.vel.y = self.jump_force.y

    def slide(self):
        if self.on_ground:
            self.state = PlayerState.SLIDE
            self.width, self.height = 120, 40

    def run(self):
        """Return to running state"""
        self.state = PlayerState.RUN
        self.width, self.height = 100, 100

    def update(self, dt):
        # Reset horizontal acceleration each frame
        self.acc = vec(0, 0)

        # Horizontal acceleration if running
        if self.state == PlayerState.RUN:
            self.acc.x = 200

        # Apply gravity if not on ground
        if not self.on_ground:
            self.acc.y = GRAVITY.y

        # Apply deceleration if colliding (reduce velocity but not below min_vel)
        MIN_VEL_X = 50  # Minimum horizontal velocity when colliding
        if self.colliding:
            # Reduce velocity towards MIN_VEL_X instead of 0
            if self.vel.x > MIN_VEL_X:
                self.acc.x = -400  # Deceleration force
            else:
                self.acc.x = 0
                self.vel.x = MIN_VEL_X

        # Handle slide duration
        if self.state == PlayerState.SLIDE:
            self.time_since_slide += dt * 1000  # convert dt to milliseconds
            if self.time_since_slide > self.slide_time:
                self.run()
                self.time_since_slide = 0

        # Update velocity
        new_vel = self.vel + self.acc * dt
        vel_x = min(new_vel.x, self.max_vel.x)
        vel_x = max(vel_x, MIN_VEL_X)  # enforce minimum horizontal speed
        self.vel = vec(vel_x, new_vel.y)  # vertical velocity from gravity/jump

        # Update position
        self.pos += self.vel * dt
