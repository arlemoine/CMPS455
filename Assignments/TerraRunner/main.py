import pygame as pg
from models.session import Session
from view.view import View
from controller.controller import Controller
import config

def main():
    pg.init()

    clock = pg.time.Clock()
    session = Session()
    view = View(session)
    controller = Controller(session)

    dt = 0
    while not controller.quit_game:
        dt = clock.tick(config.FPS) / 1000
        controller.handle_input()

        # Handle session restart requested by controller
        if getattr(controller, "restart", False):
            session = Session()            # create new session
            controller.session = session   # give controller the new session
            view.session = session         # give view the new session
            controller.restart = False

        if controller.mode == "playing" and not session.paused:
            session.update(dt)
            if session.game_over:
                controller.set_mode("game_over")
        view.render(controller, session, dt)

    pg.quit()

if __name__ == "__main__":
    main()
