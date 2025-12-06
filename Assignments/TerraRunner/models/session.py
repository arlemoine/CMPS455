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
        self.paused = False
        self.difficulty = 1
        self.max_difficulty = 10
        self.difficulty_distance_constant = 500
        self.distance_to_difficulty_up = 0

    def update(self, dt):
        # Update world
        self.world.update(dt, self.player)
        self.player.update(dt, self.world)

        # Track monster catching player
        caught = self.monster.update(dt, self.player)

        if caught:
            self.score_tracker.finalize_run()
            self.game_over = True

        self.score_tracker.update(dt, self.world.scroll_speed)

        self.distance_to_difficulty_up += self.world.scroll_speed.x * -1 * dt
        if self.distance_to_difficulty_up >= self.difficulty_distance_constant:
            self.distance_to_difficulty_up = 0
            self.increase_difficulty()

    def increase_difficulty(self):
        if self.difficulty < 25:
            self.difficulty += 1
            self.world.distance_between_obstacles = self.world.distance_between_obstacles - (self.difficulty * 5)
            self.monster.buff += 0.2
