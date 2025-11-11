import pygame as pg

from controller.controller import Controller
from models.game import Game
from view.view import View

import config

def main():
    pg.init()
    pg.mixer.init()

    # MVC
    game = Game()
    view = View()
    controller = Controller(game, view)

    clock = pg.time.Clock()

    while controller.game_running:
        dt = clock.tick(config.FPS) / 1000  # seconds
        
        # Input
        controller.handle_input(dt)
        
        # Update
        controller.update_game(dt)
        controller.update_music()
        
        # Render
        view.render(controller)

    pg.quit()

if __name__ == "__main__":
    main()
