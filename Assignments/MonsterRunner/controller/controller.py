import pygame as pg

import controller.controls as controls

class Controller:
    def __init__(self, player, menu):
        self.player = player
        self.menu = menu
        self.mode = "gameplay"

        self.configs = {
            "gameplay": (controls.GAMEPLAY_KEYDOWN, controls.GAMEPLAY_KEYUP),
            "menu": (controls.MENU_KEYDOWN, controls.MENU_KEYUP),
        }

    def set_mode(self, mode):
        if mode in self.configs:
            self.mode = mode

    def handle_event(self, event):
        keydown_map, keyup_map = self.configs[self.mode]

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
        if self.mode == "gameplay":
            func = getattr(self.player, action, None)
        elif self.mode == "menu":
            func = getattr(self.menu, action, None)

        if func:
            func()
