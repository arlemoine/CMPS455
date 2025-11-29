import pygame.math.Vector2 as vec

import config

JUMP_POWER = vec(0, -18)
GRAVITY = vec(0, 10)

class Player:
    def __init__(self):
        # Player
        self.width, self.height = 40, 100  # taller player for ducking
        self.mass = 1
        self.pos = vec(200, config.SCREEN_HEIGHT - self.height - config.GROUND_HEIGHT)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.max_vel = config.BASE_SPEED
        self.on_ground = True
        self.is_sliding = False
        self.slide_height = self.height / 2

    def update(self, dt):
        if self.on_ground:
            self.acc = vec(0, 0)
        else:
            self.acc = GRAVITY

        self.vel += self.acc * dt
        self.pos += self.vel * dt

    def jump(self):
        if self.on_ground:
            self.acc = JUMP_POWER
            self.on_ground = False
            self.is_sliding = False

    def slide(self):
        if self.on_ground:
            if not self.is_sliding:
                self.is_sliding = True
            else:
                self.is_sliding = False # Toggle off slide
