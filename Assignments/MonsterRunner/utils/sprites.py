import pygame as pg

def load_sprites(sheet_path, json_data, box_sizes):
    """
    Load sprite sheet and return dictionary of surfaces per action/state.

    sheet_path : str
        Path to sprite sheet image.
    json_data : dict
        Parsed JSON describing frames.
    box_sizes : dict
        Dict mapping state/action -> (width, height)
    """
    sheet = pg.image.load(sheet_path).convert_alpha()
    frames = json_data["frames"]

    sprites = {state: [] for state in box_sizes}

    for frame_name, frame_data in frames.items():
        rect = frame_data["frame"]
        action = frame_data.get("action", "run")
        if action not in box_sizes:
            continue  # skip unknown actions

        # Extract image from sheet
        image = sheet.subsurface((rect["x"], rect["y"], rect["w"], rect["h"]))

        # Stretch to fit the box
        box_w, box_h = box_sizes[action]
        image = pg.transform.scale(image, (box_w, box_h))

        # Crop top half for slide if needed
        if action == "slide":
            image = image.subsurface((0, box_h // 2, box_w, box_h // 2))

        sprites[action].append(image)

    return sprites
