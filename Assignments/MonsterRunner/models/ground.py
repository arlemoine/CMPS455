import config
import random
from pygame.math import Vector2 as vec

import config

class Ground:
    def __init__(self):
        self.height = 500
        self.pos = config.SCREEN_HEIGHT - 100