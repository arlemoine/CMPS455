import pygame as pg

from models.game import Game
from view.view import View

import config

class Controller:
    def __init__(self, model, view):
        self.game_running = True
        self.model = model
        self.view = view
        
    def handle_input(self, dt):
        """Handle all user input events."""
        current_time = pg.time.get_ticks()

        # Handle global events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_running = False

        # Handle continuous or mapped keys
        # keys_pressed = pg.key.get_pressed()
        # if self.state in KEY_ACTIONS:
        #     current_map = KEY_ACTIONS[self.state]
        #     for key, action_fn in current_map.items():
        #         # Use cooldown for menu/gameover inputs
        #         if keys_pressed[key]:
        #             # For menu/gameover, limit rapid repeat
        #             if self.state in (GameState.MENU, GameState.GAMEOVER):
        #                 if current_time - self.last_menu_input_time > config.MENU_COOLDOWN_MS:
        #                     action_fn(ship, model, self, dt)
        #                     self.last_menu_input_time = current_time
        #             else:
        #                 # For PLAYING keys (movement, thrust, etc.)
        #                 action_fn(ship, model, self, dt)
    
    def update_game(self, dt):
        return

    def update_music(self):
        return