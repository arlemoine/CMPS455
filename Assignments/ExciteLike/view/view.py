import pygame as pg
import config

class View:
    def __init__(self):
        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption("ExciteLike")
        self.font = pg.font.Font(None, 50)

    def render(self, controller):
        self.screen.fill(config.BLACK)