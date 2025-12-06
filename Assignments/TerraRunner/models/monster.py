from pygame.math import Vector2 as vec
import config
from models.collision import aabb

class Monster:
    def __init__(self):
        self.width = config.CELL_SIZE * 2
        self.height = config.CELL_SIZE * 3

        # Spawn off-screen to the left initially
        self.pos = vec(config.HARD_BOUND_LEFT, config.GROUND_HEIGHT - self.height)
        self.vel = vec(0, 0)  # base movement speed

        self.active = False  # only becomes active after 10 seconds
        self.spawn_timer = 0.0  # tracks time since game start

    def update(self, dt, player):
        """
        Update monster behavior:
        - Activates after 10 seconds
        - Moves forward
        - Gains extra distance when world slowed
        - Returns True if catches player
        """
        # Increment timer until spawn
        if not self.active:
            self.spawn_timer += dt
            if self.spawn_timer >= 10.0:
                self.active = True
            else:
                return False  # inactive monsters do nothing

        # Gains extra ground if player is slowed (world scroll slowed)
        if player.colliding:  # slowed
            self.vel = (config.SPEED_NORM - config.SPEED_SLOW) * config.MONSTER_SPEED_DEBUFF * -1
        else:
            self.vel = vec(0, 0)

        # Monster moves forward constantly
        self.pos += self.vel * dt

        # Check collision with player
        if aabb(self, player):
            return True

        return False
