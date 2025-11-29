# view.py
import pygame as pg
from pygame.math import Vector2 as vec
import math
import config

class View:
    def __init__(self):
        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption("ExciteLike")
        self.font = pg.font.Font(None, 50)

    # ------------------------
    # Draw a rotated box (OBB-style)
    # ------------------------
    def draw_box(self, box):
        hw = box.width / 2
        hh = box.height / 2
        rad = math.radians(getattr(box, "angle", 0))
        x_axis = vec(math.cos(rad), math.sin(rad))
        y_axis = vec(-math.sin(rad), math.cos(rad))
        pos = box.pos

        corners = [
            pos + x_axis* hw + y_axis* hh,
            pos + x_axis* hw - y_axis* hh,
            pos - x_axis* hw - y_axis* hh,
            pos - x_axis* hw + y_axis* hh
        ]

        points = [(c.x, c.y) for c in corners]
        pg.draw.polygon(self.screen, box.color, points)

    # ------------------------
    # Draw a ground segment (also supports rotation)
    # ------------------------
    def draw_ground_segment(self, ground):
        hw = ground.width / 2
        hh = ground.height / 2
        rad = math.radians(getattr(ground, "angle", 0))
        x_axis = vec(math.cos(rad), math.sin(rad))
        y_axis = vec(-math.sin(rad), math.cos(rad))
        pos = ground.pos

        corners = [
            pos + x_axis* hw + y_axis* hh,
            pos + x_axis* hw - y_axis* hh,
            pos - x_axis* hw - y_axis* hh,
            pos - x_axis* hw + y_axis* hh
        ]

        points = [(c.x, c.y) for c in corners]
        pg.draw.polygon(self.screen, getattr(ground, "color", (0,255,0)), points)

    # ------------------------
    # Render everything
    # ------------------------
    def render(self, controller):
        self.screen.fill(config.WHITE)

        self.draw_ground_segment(controller.ground)

        # Draw the player box
        self.draw_box(controller.box)

        pg.display.flip()
