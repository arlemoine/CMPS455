from models.camera import Camera
from models.collision import aabb
from models.chunk import ChunkManager
from models.player import Player

import config

class Session:
    def __init__(self):
        self.chunk_manager = ChunkManager()
        self.player = Player()
        self.camera = Camera(self.player)
        self.game_over = False
        self.score = 0

    def update(self, dt):
        # Update world
        self.chunk_manager.update(dt, self.player)
        self.player.update(dt)
        self.camera.update(dt, self.player)

        # Reset collision flags each frame
        self.player.colliding = False
        self.player.on_ground = False

        # Check collisions against active chunks
        for chunk in self.chunk_manager.chunks:
            # Ground collision
            if chunk.ground is not None:
                if aabb(self.player, chunk.ground):
                    # Snap player to top of ground and clear vertical velocity
                    self.player.on_ground = True
                    self.player.pos.y = chunk.ground.pos.y - self.player.height
                    self.player.vel.y = 0

            # Obstacle collision
            if chunk.obstacle is not None:
                if aabb(self.player, chunk.obstacle):
                    self.player.colliding = True

        # Game-over if player falls too far below the ground line
        if self.player.pos.y > (config.GROUND_HEIGHT + 500):
            self.game_over = True
