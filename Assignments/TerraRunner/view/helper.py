import pygame as pg
from pathlib import Path

def load_sprite(path, width=None, height=None):
    # Ensure path is a string or Path object
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Sprite file not found: {path}")

    img = pg.image.load(str(path)).convert_alpha()

    if width and height:
        img = pg.transform.scale(img, (int(width), int(height)))
    return img
