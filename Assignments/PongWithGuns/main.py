import pygame as pg
from model import PongModel
from view import PongView
from controller import PongController

pg.init()
pg.mixer.init() 
view = PongView()
model = PongModel(view.SCREEN_WIDTH, view.SCREEN_HEIGHT)
controller = PongController(model)

clock = pg.time.Clock()
running = True

# Main game loop
while running:
    # Handle Input (including QUIT and RESTART)
    running = controller.handle_input()
    if not running:
        break

    dt = clock.tick(60) / 1000.0 # 60 FPS cap, msec to sec

    controller.update_game_state(dt)

    view.render(controller.model, controller.score, controller.game_running) 

view.quit()

