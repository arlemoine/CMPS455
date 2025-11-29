import config
import pygame.math.Vector2 as vec

class Camera:
    def __init__(self):
        self.width, self.height = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        self.pos = vec(0, 0)
        self.offset = 250
