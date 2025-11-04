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
        self.menus = {
            "main": {0: "Play", 1: "Quit"},
            "gameover": {0: "Continue", 1: "Quit"}
        }
        self.active_menu = "main" 
        self.menu_choice_index = 0

        self.last_menu_input_time = 0

        self.sound_main_menu = pg.mixer.Sound('assets/main_menu.wav')
        self.sound_in_game = pg.mixer.Sound('assets/in_game.wav')

        # Create a dedicated channel for background music
        self.music_channel = pg.mixer.Channel(0)
        self.current_music = None

    def handle_input(self, ship, model, dt):
        """Handle all user input events."""
        current_time = pg.time.get_ticks()

        # Handle global events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_running = False

        # Handle continuous or mapped keys
        keys_pressed = pg.key.get_pressed()
        if self.state in KEY_ACTIONS:
            current_map = KEY_ACTIONS[self.state]
            for key, action_fn in current_map.items():
                # Use cooldown for menu/gameover inputs
                if keys_pressed[key]:
                    # For menu/gameover, limit rapid repeat
                    if self.state in (GameState.MENU, GameState.GAMEOVER):
                        if current_time - self.last_menu_input_time > config.MENU_COOLDOWN_MS:
                            action_fn(ship, model, self, dt)
                            self.last_menu_input_time = current_time
                    else:
                        # For PLAYING keys (movement, thrust, etc.)
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
        """Update the game state."""
        if self.state == GameState.PLAYING:
            trigger = self.model.update(dt)
            if trigger == -1:
                self.toggle_gameover()  # Switch to GAMEOVER once
        elif self.state == GameState.GAMEOVER:
            # Still update the model, but ignore repeated death triggers
            self.model.update(dt)
        elif self.state == GameState.MENU:
            self.model.menu_update(dt)

    def menu_up(self):
        """Move up one selection in the current active menu."""
        current_time = pg.time.get_ticks()
        if current_time - self.last_menu_input_time > config.MENU_COOLDOWN_MS:
            menu = self.menus[self.active_menu]
            self.menu_choice_index -= 1
            if self.menu_choice_index < 0:
                self.menu_choice_index = len(menu) - 1
            self.last_menu_input_time = current_time

    def menu_down(self):
        """Move down one selection in the current active menu."""
        current_time = pg.time.get_ticks()
        if current_time - self.last_menu_input_time > config.MENU_COOLDOWN_MS:
            menu = self.menus[self.active_menu]
            self.menu_choice_index += 1
            if self.menu_choice_index >= len(menu):
                self.menu_choice_index = 0
            self.last_menu_input_time = current_time


    def menu_select(self):
        """Execute the currently selected menu option."""
        menu = self.menus[self.active_menu]
        selected_option = menu[self.menu_choice_index]

        if selected_option == "Play":
            self.state = GameState.PLAYING
            self.active_menu = "main"
            self.menu_choice_index = 0

        elif selected_option == "Quit":
            self.game_running = False

        elif selected_option == "Continue":
            # Reset everything to go back to main menu
            self.state = GameState.MENU
            self.active_menu = "main"
            self.menu_choice_index = 0

            # Fully reset the model (new ship, asteroids, explosions, etc.)
            ship_type = getattr(self.model.ship, "ship_type", "default")
            self.model.__init__(ship_type)

    def toggle_gameover(self):
        """Switch to the game over screen."""
        self.state = GameState.GAMEOVER
        self.active_menu = "gameover"
        self.menu_choice_index = 0

    def play_music(self, sound, label):
        """Play a looping background track on the music channel only."""
        if self.current_music != label:
            self.music_channel.stop()          # stop only music, not SFX
            self.music_channel.play(sound, loops=-1)
            self.current_music = label

    def update_music(self):
        """Switch background music based on game state."""
        if self.state == GameState.MENU:
            self.play_music(self.sound_main_menu, "main_menu")
        elif self.state in (GameState.PLAYING, GameState.GAMEOVER):
            self.play_music(self.sound_in_game, "in_game")
        elif self.state == GameState.PAUSED:
            pass
