from pygame.math import Vector2 as vec
import random

import config
from models.ground import GroundSegment
from models.obstacle import Obstacle
from models.player import Player


class Chunk:
    def __init__(self, x, ground, obstacle):
        self.ground = ground
        self.obstacle = obstacle
        self.x = x

class ChunkManager:
    def __init__(self):
        self.chunks = []
        self.next_chunk_x = 0
        self.chunk_width = config.CHUNK_WIDTH
        self.chunk_spawn_distance = 500
        self.previous_chunk = None
    
    def update(self, dt, player):
        # 1. Generate chunks ahead
        while self.next_chunk_x < player.pos.x + self.chunk_spawn_distance:
            self.generate_chunk(self.previous_chunk)

        # 2. Remove old chunks
        self.chunks = [
            c for c in self.chunks
            if c.x + self.chunk_width >= player.pos.x - self.chunk_spawn_distance
        ]

    def generate_chunk(self, previous_chunk=None):

        # Always safe to check
        if (previous_chunk is None or 
            previous_chunk.ground is None or 
            previous_chunk.obstacle is not None):

            ground = GroundSegment(self.chunk_width, vec(self.next_chunk_x, config.GROUND_HEIGHT))
            obstacle = None

        else:
            choice = random.choice(["hole", "jump", "slide"])

            if choice == "hole":
                ground = None
                obstacle = None

            elif choice == "jump":
                ground = GroundSegment(self.chunk_width, vec(self.next_chunk_x, config.GROUND_HEIGHT))
                obstacle = Obstacle(self.chunk_width, vec(self.next_chunk_x, config.GROUND_HEIGHT - 50))

            elif choice == "slide":
                ground = GroundSegment(self.chunk_width, vec(self.next_chunk_x, config.GROUND_HEIGHT))
                obstacle = Obstacle(self.chunk_width, vec(self.next_chunk_x, config.GROUND_HEIGHT - 100))

        chunk = Chunk(self.next_chunk_x, ground, obstacle)
        self.chunks.append(chunk)
        self.previous_chunk = chunk
        self.next_chunk_x += self.chunk_width
        return chunk
