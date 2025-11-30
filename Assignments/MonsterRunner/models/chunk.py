from pygame.math import Vector2 as vec
import random

import config
from models.ground import GroundSegment
from models.obstacle import Obstacle
from models.player import Player



class Chunk:
    def __init__(self, x_start):
        self.width = 50
        self.x_start = 0
        self.ground = None
        self.obstacle = None

    def generate(self, previous_chunk=None):
        """
        Randomly decide what goes into this chunk.
        """
        blacklisted_types = []

        # If last chunk was a hole, do a flat ground segment with no obstacle
        if previous_chunk.ground is None:
            obstacle = None
            ground = GroundSegment(self.width, vec(self.x_start, config.GROUND_HEIGHT))
        # If last chunk had flat ground with no obstacle - create obstacle or hole
        elif previous_chunk.obstacle is None:
            choice = random.choice(["hole", "jump", "slide"])
            if choice == "hole":
                obstacle = None
                ground = None
            elif choice == "jump":
                obstacle = Obstacle(self.width, config.GROUND_HEIGHT - )


        # Shift x position of next chunk
        self.x_start += self.width