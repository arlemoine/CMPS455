from pygame.math import Vector2 as vec
import random

import config
from models.grid import get_cell_index

normal_speed = vec(-300, 0)
slow_speed = vec(-100, 0)

class World:
    def __init__(self):
        self.blocks = [] # Holds all blocks
        self.ground_blocks = [] # Holds ground blocks only
        self.obstacle_blocks = [] # Holds obstacle blocks only
        self.scroll_speed = vec(-300, 0)
        self.grid_cells = {}  # key: (grid_x, grid_y), value: list of blocks
        self.distance_between_obstacles = 500

        # Generate ground initially
        self.gen_ground(0, config.GROUND_HEIGHT)
        self.extend_ground()

    def update(self, dt, player):
        if player.colliding:
            self.scroll_speed = slow_speed
        else:
            self.scroll_speed = normal_speed

        delete_queue = []
        for block in self.blocks:
            if not self.update_block(block, dt):
                delete_queue.append(block)

        # Remove blocks scheduled for deletion
        for block in delete_queue:
            self.remove_block(block)

        # Add obstacles
        self.add_obstacles_if_needed()

        self.extend_ground()

    def update_block(self, block, dt):
        """Handles movement, grid update, and returns False if block should be removed"""
        old_cell = (block.grid_x, block.grid_y)

        self.move_block(block, dt)
        in_grid_bounds = block.update_grid_pos()
        new_cell = (block.grid_x, block.grid_y)

        if not in_grid_bounds:
            return False  # block is off-grid

        if old_cell != new_cell:
            self.move_to_new_cell(block, old_cell, new_cell)

        return True

    def move_block(self, block, dt):
        block.pos += self.scroll_speed * dt

    def move_to_new_cell(self, block, old_cell, new_cell):
        self.remove_from_cell(block, old_cell)
        self.add_to_cell(block)

    def add_to_cell(self, block):
        cell = (block.grid_x, block.grid_y)
        self.grid_cells.setdefault(cell, []).append(block)

    def remove_from_cell(self, block, cell):
        if cell in self.grid_cells and block in self.grid_cells[cell]:
            self.grid_cells[cell].remove(block)

    def remove_block(self, block):
        self.remove_from_cell(block, (block.grid_x, block.grid_y))
        self.blocks.remove(block)
        if block.block_type == "ground":
            self.ground_blocks.remove(block)
        elif block.block_type == "obstacle":
            self.obstacle_blocks.remove(block)

        return block

    def gen_ground(self, x, y):
        new_block = Block("ground", x, y)
        self.blocks.append(new_block)
        self.ground_blocks.append(new_block)
        self.add_to_cell(new_block)
        return new_block

    def gen_obstacle(self, x, y):
        new_block = Block("obstacle", x, y)
        self.blocks.append(new_block)
        self.obstacle_blocks.append(new_block)
        self.add_to_cell(new_block)
        return new_block

    def get_nearby_blocks(self, grid_x, grid_y, radius=1):
        """Return all blocks in the cells within `radius` of (grid_x, grid_y)"""
        nearby_blocks = []

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                cell = (grid_x + dx, grid_y + dy)
                if cell in self.grid_cells:
                    nearby_blocks.extend(self.grid_cells[cell])

        return nearby_blocks

    def extend_ground(self):
        """Helper to add new ground blocks as world scrolls"""
        last_block = self.ground_blocks[-1]
        while last_block.pos.x + last_block.width < config.HARD_BOUND_RIGHT:
            new_block = self.gen_ground(last_block.pos.x + last_block.width, config.GROUND_HEIGHT)
            last_block = new_block

    def add_obstacles_if_needed(self):
        if not self.obstacle_blocks:
            last_x = 0
        else:
            last_x = max(b.pos.x for b in self.obstacle_blocks)

        # Spawn a new obstacle if last one is far enough to the left
        if last_x < config.HARD_BOUND_RIGHT - self.distance_between_obstacles:
            ground_y = self.ground_blocks[-1].pos.y

            options = ["jump", "slide"]
            choice = random.choice(options)

            dy = 0
            if choice == "jump":
                dy = config.CELL_SIZE
            elif choice == "slide":
                dy = config.CELL_SIZE * 2

            obstacle_x = config.HARD_BOUND_RIGHT
            obstacle_y = ground_y - dy  # obstacle sits on ground
            self.gen_obstacle(obstacle_x, obstacle_y)

class Block:
    def __init__(self, block_type, x, y):
        self.width = self.height = config.CELL_SIZE
        self.pos = vec(x, y)
        self.grid_x, self.grid_y = None, None
        self.update_grid_pos()
        self.block_type = block_type

    def update_grid_pos(self):
        self.grid_x, self.grid_y = get_cell_index(self.pos.x, self.pos.y)
        
        # Track if block is outside of grid for potential removal
        if self.grid_x == -1 or self.grid_y == -1:
            return False
        else:
            return True