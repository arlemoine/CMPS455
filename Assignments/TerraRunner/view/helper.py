import pygame as pg
import os

# --- Simple in-memory cache so images are only loaded once ---
_image_cache = {}


def load_image(path, colorkey=None, convert_alpha=True):
    """
    Loads an image from disk with optional color keying.
    Uses a global cache to avoid reloading the same image multiple times.

    Args:
        path (str): Path to the image file.
        colorkey (tuple or None): RGB color to treat as transparent.
        convert_alpha (bool): Whether to preserve alpha transparency.

    Returns:
        pg.Surface: The loaded image.
    """
    if path in _image_cache:
        return _image_cache[path]

    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")

    image = pg.image.load(path)

    if convert_alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()

    if colorkey is not None:
        image.set_colorkey(colorkey)

    _image_cache[path] = image
    return image


def load_and_scale(path, size, colorkey=None, convert_alpha=True):
    """
    Loads an image and scales it to a new size.

    Args:
        path (str): Image path.
        size (tuple): (width, height).
        colorkey (tuple or None): Optional transparency key.

    Returns:
        pg.Surface
    """
    img = load_image(path, colorkey, convert_alpha)
    return pg.transform.scale(img, size)


def load_spritesheet(path, sprite_width, sprite_height,
                     colorkey=None, convert_alpha=True):
    """
    Splits a sprite sheet into individual frames.

    Args:
        path (str): File location.
        sprite_width (int): Width of each frame.
        sprite_height (int): Height of each frame.

    Returns:
        list[pg.Surface]: List of frames.
    """
    sheet = load_image(path, colorkey, convert_alpha)
    sheet_w, sheet_h = sheet.get_size()

    frames = []
    for y in range(0, sheet_h, sprite_height):
        for x in range(0, sheet_w, sprite_width):
            frame = sheet.subsurface((x, y, sprite_width, sprite_height))
            frames.append(frame.copy())

    return frames


def render_text(text, font, color=(255, 255, 255)):
    """
    Renders text using a given font and color.

    Args:
        text (str): Text to render.
        font (pg.font.Font): Loaded font object.
        color (tuple): RGB color.

    Returns:
        pg.Surface
    """
    return font.render(text, True, color)
