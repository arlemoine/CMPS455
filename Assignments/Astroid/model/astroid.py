import math
import random

import config

class Astroid:
    def __init__(self, x, y, size: int = 3):
        self.sprite_index = random.randrange(4)

        self.x = x
        self.y = y
        self.size = size
        self.radius = 0
        self.calc_radius()

        self.angle = 0
        self.rotation_speed = random.uniform(-1, 1) * config.ASTROID_ROTATION_SPEED # Randomize spin direction
        self.vx = random.randrange(-11, 12, 2) # Speed controlled by a fractional config for rotation speed
        self.vy = random.randrange(-11, 12, 2)

    def calc_radius(self):
        self.radius = self.size * 15

    def update(self, dt):
        self.x += self.vx * dt * config.ASTROID_MOVEMENT_SPEED
        self.y += self.vy * dt * config.ASTROID_MOVEMENT_SPEED
        self.angle += self.rotation_speed * dt
        self.angle %= 360

        if (
            self.x < config.HARD_BOUNDARY_LEFT or
            self.x > config.HARD_BOUNDARY_RIGHT or
            self.y < config.HARD_BOUNDARY_TOP or
            self.y > config.HARD_BOUNDARY_BOTTOM
        ):
            return False
        else: 
            return True

    def bounce_off(self, other):
        """Elastic collision between self and other asteroid."""
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return

        # Normal vector
        nx = dx / distance
        ny = dy / distance

        # Tangent vector
        tx = -ny
        ty = nx

        # Project velocities onto normal and tangent
        v1n = self.vx * nx + self.vy * ny
        v1t = self.vx * tx + self.vy * ty
        v2n = other.vx * nx + other.vy * ny
        v2t = other.vx * tx + other.vy * ty

        # Swap normal components
        v1n, v2n = v2n, v1n

        # Convert scalar normal/tangent velocities back to vectors
        self.vx = v1n * nx + v1t * tx
        self.vy = v1n * ny + v1t * ty
        other.vx = v2n * nx + v2t * tx
        other.vy = v2n * ny + v2t * ty
