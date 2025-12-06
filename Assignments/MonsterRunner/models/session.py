from models.collision import aabb
from models.monster import Monster
from models.player import Player
from models.scoring import ScoreTracker
from models.world import World

import config

class Session:
    def __init__(self):
        self.player = Player()
        self.monster = Monster()
        self.world = World()
        self.score_tracker = ScoreTracker()
        self.game_over = False
        self.score = 0

    def update(self, dt):
        # Update world
        self.world.update(dt, self.player)
        self.player.update(dt, self.world)

        # Track monster catching player
        caught = self.monster.update(dt, self.player)

        if caught:
            self.score.finalize_run()
            self.game_over = True

        self.score_tracker.update(dt, self.world.scroll_speed)