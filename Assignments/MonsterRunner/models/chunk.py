from pygame.math import Vector2 as vec

import config
from models.ground import GroundSegment
from models.obstacle import Obstacle
from models.player import Player

class Chunk:
    def __init__(self, x_start):
        self.width = 50
        self.x_start = x_start
        self.ground = None
        self.obstacle = None

    def generate(self, previous_chunk=None):
        """
        Randomly decide what goes into this chunk.
        """
        