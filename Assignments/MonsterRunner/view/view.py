import pygame as pg

import config
import models.grid as grid

class View:
    def __init__(self):
        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption("MonsterRunner")
        self.font = pg.font.Font(None, 50)

    def draw_grid(self):
        """
        Draws the entire grid on the given Pygame surface.
        """
        for i in range(grid.num_cells_x):
            for j in range(grid.num_cells_y):
                x0, y0, x1, y1 = grid.get_cell_bounds(i, j)
                rect = pg.Rect(x0, y0, config.CELL_SIZE, config.CELL_SIZE)
                pg.draw.rect(self.screen, config.SILVER, rect, width=1)

    def draw_world_blocks(self, session):
        world = session.world

        for block in world.blocks:

            if block.block_type == "ground": block_color = config.GREEN
            elif block.block_type == "obstacle": block_color = config.RED
            else: block_color = config.BLACK

            pg.draw.rect(self.screen, block_color, (block.pos.x, block.pos.y, block.width, block.height))

    def draw_player(self, session):
        player = session.player
        pg.draw.rect(self.screen, config.BLUE, (player.pos.x, player.pos.y, player.width, player.height))

    def render(self, session):
        self.screen.fill(config.WHITE)

        self.draw_grid()
        self.draw_world_blocks(session)
        self.draw_player(session)

        pg.display.flip()
