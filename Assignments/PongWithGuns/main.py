import pygame as pg
from model import PongModel
from view import PongView
from controller import PongController

pg.init()
view = PongView()
model = PongModel(view.SCREEN_WIDTH, view.SCREEN_HEIGHT)
controller = PongController(model)

clock = pg.time.Clock()
running = True

# Main game loop
while running:
    running = controller.handle_input()
    if not running:
        break

    dt = clock.tick(60) / 1000.0 # 60 FPS cap, msec to sec

    model.update(dt)

    view.render(model)

view.quit()

