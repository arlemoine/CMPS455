from pygame.math import Vector2 as vec

import config 

def check_collision_obstacle(a, b):
    # Get b's values from the dictionary
    b_pos = b["pos"]
    b_width = b["width"]
    b_height = b["height"]

    # AABB collision check
    if a.pos.x + a.width  < b_pos.x: return False  # a is left of b
    if a.pos.x > b_pos.x + b_width: return False  # a is right of b
    if a.pos.y + a.height < b_pos.y: return False  # a is above b
    if a.pos.y > b_pos.y + b_height: return False  # a is below b

    return True

def check_collision_ground(a, b):
    # Get b's values from the dictionary
    b_pos = b["pos"]
    b_width = b["width"]
    b_height = b["height"]

    # AABB collision check
    if a.pos.x + a.width  < b_pos.x: return False  # a is left of b
    if a.pos.x > b_pos.x + b_width: return False  # a is right of b
    if a.pos.y + a.height < b_pos.y: return False  # a is above b
    if a.pos.y > b_pos.y + b_height: return False  # a is below b

    return True

