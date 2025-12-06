import pygame as pg
from models.session import Session
from view.view import View
from controller.controller import Controller
import config

def main():
    pg.init()

    clock = pg.time.Clock()
    view = View()
    session = Session()
    controller = Controller(session)

    dt = 0
    while not session.game_over:
        dt = clock.tick(config.FPS) / 1000
        controller.handle_input()
        if controller.mode == "playing" and not session.paused:
            session.update(dt)
        view.render(controller, session)

    pg.quit()

if __name__ == "__main__":
    main()
