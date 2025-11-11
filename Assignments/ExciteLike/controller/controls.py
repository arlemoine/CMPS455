import pygame as pg
from .enum import GameState

# Defines key maps per game state with lambdas
KEY_ACTIONS = {
    GameState.PLAYING: {
        pg.K_LEFT: lambda ship, model, controller, dt: ship.rotate(dt, -1),
        pg.K_RIGHT: lambda ship, model, controller, dt: ship.rotate(dt, 1),
        pg.K_UP: lambda ship, model, controller, dt: ship.thrust(dt),
        pg.K_DOWN: lambda ship, model, controller, dt: ship.brake(dt),
        pg.K_SPACE: lambda ship, model, controller, dt: model.ship.fire_bullet(),
        pg.K_ESCAPE: lambda ship, model, controller, dt: controller.toggle_pause()
    },
    GameState.MENU: {
        pg.K_UP: lambda ship, model, controller, dt: controller.menu_up(),
        pg.K_DOWN: lambda ship, model, controller, dt: controller.menu_down(),
        pg.K_RETURN: lambda ship, model, controller, dt: controller.menu_select()
    },
    GameState.PAUSED: {
        pg.K_ESCAPE: lambda ship, model, controller, dt: controller.toggle_pause()
    },
    GameState.GAMEOVER: {
        pg.K_UP: lambda ship, model, controller, dt: controller.menu_up(),
        pg.K_DOWN: lambda ship, model, controller, dt: controller.menu_down(),
        pg.K_RETURN: lambda ship, model, controller, dt: controller.menu_select()
    },
}
