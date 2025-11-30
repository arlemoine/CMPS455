from models.camera import Camera
from models.collision import check_collision_obstacle, check_collision_ground
from models.ground import Ground
from models.obstacle import Obstacle
from models.player import Player

import config

class Session:
    def __init__(self):
        self.ground = Ground()
        self.player = Player()
        self.camera = Camera(self.player)
        self.obstacles = Obstacle()
        self.game_over = False
        self.score = 0

    def update(self, dt):
        self.ground.update(dt, self.player)
        self.player.update(dt)
        self.camera.update(dt, self.player)
        self.obstacles.update(dt, self)

        # Detect player-obstacle collision
        collision = False
        for obstacle in self.obstacles.obstacle_list:
            player_obstacle_collision = check_collision_obstacle(self.player, obstacle)
            if player_obstacle_collision:
                collision = True
                break
        if collision:
            self.player.colliding = True
        else:
            self.player.colliding = False

        # Detect player-ground collision
        collision = False
        for segment in self.ground.segment_list:
            player_ground_collision = check_collision_ground(self.player, segment)
            if player_ground_collision:
                collision = True
                self.player.on_ground = True
                self.player.pos.y = segment["pos"].y - self.player.height
                break

        if self.player.pos.y > (config.GROUND_HEIGHT + 500):
            self.game_over = True