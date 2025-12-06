from enum import Enum
import pygame as pg
from pygame.math import Vector2 as vec

import config
from models.collision import aabb
from models.grid import get_cell_index

GRAVITY = vec(0, 2000)
JUMP_FORCE = vec(0, -1000)
run_width, run_height = config.CELL_SIZE * 1.2, config.CELL_SIZE * 2
slide_width, slide_height = config.CELL_SIZE * 2, config.CELL_SIZE * 0.8
jump_width, jump_height = config.CELL_SIZE * 1.2, config.CELL_SIZE * 1.6
SCREEN_CENTER = vec(config.SCREEN_WIDTH / 2, config.SCREEN_WIDTH / 2)

class PlayerState(Enum):
    RUN = 0
    JUMP = 1
    SLIDE = 2

class Player:
    def __init__(self):
        self.width, self.height = run_width, run_height
        self.state = PlayerState.RUN
        self.pos = vec(SCREEN_CENTER.x + config.PLAYER_OFFSET.x, SCREEN_CENTER.y + config.PLAYER_OFFSET.y)
        self.grid_x, self.grid_y = None, None
        self.update_grid_pos()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.slide_time = config.SLIDE_DISTANCE / self.vel.x
        self.max_vel = vec(100, 0)
        self.on_ground = True
        self.time_since_slide = 0
        self.colliding = False
        self.dh = run_height - slide_height

    def jump(self):
        if self.on_ground:
            self.state = PlayerState.JUMP
            self.width, self.height = jump_width, jump_height
            self.on_ground = False
            self.vel.y = JUMP_FORCE.y

    def slide(self):
        if self.on_ground and self.state != PlayerState.SLIDE:
            self.state = PlayerState.SLIDE
            self.width, self.height = slide_width, slide_height
            self.pos.y += self.dh  # lower player
            self.time_since_slide = 0  # reset timer

    def run(self):
        """Return to running state"""
        if self.state != PlayerState.RUN:
            # Raise player to match new height
            self.pos.y -= run_height - self.height
            self.width, self.height = run_width, run_height
            self.state = PlayerState.RUN
            self.time_since_slide = 0

    def update(self, dt, world):
        # Reset acceleration each frame
        self.acc = vec(0, 0)
        # Reset colliding each frame
        self.colliding = False
        # Apply gravity if not on ground
        if not self.on_ground:
            self.acc.y = GRAVITY.y
        # Update velocity
        self.vel = vec(0, self.vel.y + self.acc.y * dt)  # vertical velocity only

        # Update position and grid information
        self.pos += self.vel * dt
        player_in_bounds = self.update_grid_pos()
        neighboring_blocks = world.get_nearby_blocks(self.grid_x, self.grid_y, 2)

        # Update sliding
        if self.state == PlayerState.SLIDE:
            self.time_since_slide += dt * 1000  # convert dt to milliseconds
            if self.time_since_slide >= self.slide_time:
                self.run()

        # Perform collision checks with neighboring blocks
        for block in neighboring_blocks:
            if aabb(self, block):
                self.handle_collision(block)

        # Track if player has left the bounds of the grid (i.e. has fallen through a hole and "died")
        return player_in_bounds

    def update_grid_pos(self):
        self.grid_x, self.grid_y = get_cell_index(self.pos.x, self.pos.y)
        if self.grid_x == -1 or self.grid_y == -1:
            return False
        return True

    def handle_collision(self, block):
        # Stop the player on the ground
        if block.block_type == "ground":
            self.on_ground = True
            self.pos.y = block.pos.y - self.height
            self.vel.y = 0

        if block.block_type == "obstacle":
            self.colliding = True

