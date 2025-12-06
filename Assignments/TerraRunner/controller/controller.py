import pygame as pg

import controller.controls as controls
from models.session import Session
from view.view import View

class Controller:
    def __init__(self, session):
        self.session = session
        self.mode = "menu"

        # Main menu info
        self.main_menu_options = ["PLAY", "WARDROBE", "QUIT"]
        self.main_menu_hover = "PLAY"

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
        if action == "pause_toggle":
            self.session.paused = not self.session.paused
        
        if self.mode == "playing":
            func = getattr(self.session.player, action, None)
            if func:
                func()
        elif self.mode == "menu":
            if action == "menu_down":
                self.main_menu_hover = self.menu_down(self.main_menu_hover, self.main_menu_options)
            elif action == "menu_up":
                self.main_menu_hover = self.menu_up(self.main_menu_hover, self.main_menu_options)
            elif action == "menu_select":
                self.select_main_menu_option()
            # elif action == "menu_back":
            #     self.handle_menu_back()


    def menu_down(self, hovered_item, item_list):
        # Find index of current hovered item
        i = item_list.index(hovered_item)

        # Move to next item, wrap around if at end
        i = (i + 1) % len(item_list)

        return item_list[i]
            
    def menu_up(self, hovered_item, item_list):
        # Find index of current hovered item
        i = item_list.index(hovered_item)

        # Move to previous item, wrap around if at end
        i = (i - 1) % len(item_list)

        return item_list[i]

    def select_main_menu_option(self):
        if self.main_menu_hover == "PLAY":
            self.set_mode("playing")
        elif self.main_menu_hover == "QUIT":
            self.session.game_over = True
        # elif self.main_menu_hover == "WARDROBE":
        #     self.open_wardrobe_screen()
