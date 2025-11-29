import pygame as pg

# Gameplay controls
GAMEPLAY_KEYDOWN = {
    pg.K_w: "jump",
    pg.K_SPACE: "jump",
    pg.K_s: "slide",
    pg.K_LSHIFT: "dash",
}

GAMEPLAY_KEYUP = {
    pg.K_s: "slide",
}

# Menu controls
MENU_KEYDOWN = {
    pg.K_UP: "menu_up",
    pg.K_DOWN: "menu_down",
    pg.K_RETURN: "menu_select",
    pg.K_ESCAPE: "menu_back",
}

MENU_KEYUP = {}  # often empty for menus
