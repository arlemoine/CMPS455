import pygame as pg

import controller.controls as controls
from models.session import Session
from view.view import View

class Controller:
    def __init__(self, session):
        self.session = session
        self.mode = "playing"

        self.configs = {
            "playing": (controls.PLAYING_KEYDOWN, controls.PLAYING_KEYUP),
            "menu": (controls.MENU_KEYDOWN, controls.MENU_KEYUP),
        }

    def set_mode(self, mode):
        if mode in self.configs:
            self.mode = mode

    def handle_input(self):
        keydown_map, keyup_map = self.configs[self.mode]

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.session.game_over = True

            if event.type == pg.KEYDOWN:
                action = keydown_map.get(event.key)
                if action:
                    self.execute(action)

            elif event.type == pg.KEYUP:
                action = keyup_map.get(event.key)
                if action:
                    self.execute(action)

    def execute(self, action):
        """Lookup method on player/menu depending on mode."""
        func = None
        if self.mode == "playing":
            func = getattr(self.session.player, action, None)
        # elif self.mode == "menu":
        #     func = getattr(self.session.menu, action, None)

        if func:
            func()