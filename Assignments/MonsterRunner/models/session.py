from models.collision import aabb
from models.player import Player
from models.world import World

import config

class Session:
    def __init__(self):
        self.player = Player()
        self.world = World()
        self.game_over = False
        self.score = 0

    def update(self, dt):
        # Update world
        self.world.update(dt, self.player)
        self.player.update(dt, self.world)
