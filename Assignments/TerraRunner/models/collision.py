from pygame.math import Vector2 as vec

def aabb(a, b):
    """Axis-Aligned Bounding Box collision check between two game objects."""

    if a.pos.x + a.width  < b.pos.x: return False  # a is left of b
    if a.pos.x > b.pos.x + b.width: return False  # a is right of b
    if a.pos.y + a.height < b.pos.y: return False  # a is above b
    if a.pos.y > b.pos.y + b.height: return False  # a is below b

    return True
