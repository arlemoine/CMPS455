import pygame as pg
from model import PongModel
from view import PongView
from controller import PongController

# Initialize pygame and mixer
pg.init()
pg.mixer.init()

# Initialize MVC components
view = PongView()
model = PongModel(view.SCREEN_WIDTH, view.SCREEN_HEIGHT)
controller = PongController(model)

clock = pg.time.Clock()
running = True

# Main game loop
while running:
    # Handle input (movement, shooting, quit, restart)
    running = controller.handle_input()
    if not running:
        break

    # Time delta in seconds (frame-independent movement)
    dt = clock.tick(90) / 1000.0  # 60 FPS cap

    # Update game logic (model)
    controller.update_game_state(dt) 

    # Render everything (view)
    view.render(controller.model, controller.score, controller.game_running)

# Quit pygame cleanly
view.quit()
