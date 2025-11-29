import pygame.math.Vector2 as vec

import config

class Monster:
    def __init__(self):
        self.width, self.height = 60, 100
        self.pos = vec(50, config.SCREEN_HEIGHT - self.height - config.GROUND_HEIGHT)
        self.vel = config.BASE_SPEED  # match player's top speed