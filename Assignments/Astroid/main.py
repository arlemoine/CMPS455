import pygame as pg
import config
from model.model import Model
from model.ship_type import ShipType
from view.view import View
from controller.controller import Controller

def main():
    pg.init()
    pg.mixer.init()  # optional for sounds

    # MVC
    model = Model(ShipType.RED)
    view = View()
    controller = Controller(model, view)

    clock = pg.time.Clock()

    while controller.game_running:
        dt = clock.tick(config.FPS) / 1000  # seconds
        
        # Input
        controller.handle_input(model.ship, model, dt)
        
        # Update
        controller.update_game(dt)
        
        # Render
        view.render(controller, model)

    pg.quit()

if __name__ == "__main__":
    main()
