import config
from pygame.math import Vector2 as vec

class Camera:
    def __init__(self, player):
        self.width, self.height = config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        self.offset = vec(200, 500)
        self.pos = vec(player.pos.x - self.offset.x, player.pos.y - self.offset.y)

    def update(self, dt, player):
        self.pos = vec(player.pos.x - self.offset.x, player.pos.y - self.offset.y)

    def apply(self, pos):
        """Convert a world position to a screen position"""
        return pos - self.pos # pos and self.pos are Vector2