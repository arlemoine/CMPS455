import pygame as pg
from controller.controls import KEY_ACTIONS
from controller.game_state import GameState
import config

class Controller:
    """Controller for Asteroid."""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.game_running = True
        self.state = GameState.MENU
        self.menu_options = [
            "Play",
            "Quit"
        ]
        self.menu_choice = 0 # Index of menu_options[]

        self.last_menu_input_time = 0

        # self.game_mode = None
        # self.score = [0, 0]
        # self.MAX_SCORE = 2

        # --- SOUNDS ---
        # pg.mixer.init()
        # self.sound_round_start = pg.mixer.Sound('assets/round_start.mp3')
        # pg.mixer.Sound.play(self.sound_round_start)

    def handle_input(self, ship, model, dt):
        # 1️⃣ Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_running = False                
            elif event.type == pg.KEYDOWN:
                if self.state == GameState.MENU and event.key == pg.K_RETURN:
                    self.menu_select()

        # 2️⃣ Handle continuous keys (after pumping events)
        keys_pressed = pg.key.get_pressed()
        if self.state in KEY_ACTIONS:
            current_map = KEY_ACTIONS[self.state]
            for key, action_fn in current_map.items():
                if keys_pressed[key]:
                    action_fn(ship, model, self, dt)

    def toggle_pause(self):
        current_time = pg.time.get_ticks()

        if current_time - self.last_menu_input_time > config.MENU_COOLDOWN_MS:
            if self.state == GameState.PLAYING:
                self.state = GameState.PAUSED
            elif self.state == GameState.PAUSED:
                self.state = GameState.PLAYING

        self.last_menu_input_time = current_time

    def update_game(self, dt):
        '''Update the game state.'''
        if self.state == GameState.PLAYING: 
            self.model.update(dt)
        elif self.state == GameState.MENU:
            self.model.menu_update(dt)

    def menu_up(self):
        '''Go up by 1 selection in the main menu.'''
        current_time = pg.time.get_ticks()
        
        if current_time - self.last_menu_input_time > config.MENU_COOLDOWN_MS:
            self.menu_choice -= 1
            if self.menu_choice < 0:
                self.menu_choice = len(self.menu_options) - 1 # Wrap around
            
            # Reset timer after successful move
            self.last_menu_input_time = current_time 

    def menu_down(self):
        '''Go down by 1 selection in the main menu.'''
        current_time = pg.time.get_ticks()
        
        if current_time - self.last_menu_input_time > config.MENU_COOLDOWN_MS:
            self.menu_choice += 1
            if self.menu_choice >= len(self.menu_options):
                self.menu_choice = 0 # Wrap around
            
            # Reset timer after successful move
            self.last_menu_input_time = current_time 

    def menu_select(self):
        '''Choose current menu option selection.'''
        option = self.menu_options[self.menu_choice]
        
        if option == "Play":
            self.state = GameState.PLAYING
        elif option == "Quit":
            self.game_running = False

