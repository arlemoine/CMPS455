from pygame.math import Vector2 as vec
import config
from models.collision import aabb

class Monster:
    def __init__(self):
        self.width = config.CELL_SIZE * 5
        self.height = config.CELL_SIZE * 9
        self.buff = 1

        # Spawn off-screen to the left initially
        self.pos = vec(config.HARD_BOUND_LEFT, config.GROUND_HEIGHT - self.height)
        self.vel = vec(0, 0)  # base movement speed

        self.active = False  # only becomes active after 10 seconds
        self.spawn_timer = 0.0  # tracks time since game start

        # Animations
        self.time_since_run_flip = 0
        self.flip_time = 0.5 # ms
        self.run_frame = 0

        # Spawn message
        self.spawn_msg = {
            "text": "The ancient spirits of light and dark have been released...",
            "alpha": 0,        # transparency
            "timer": 0,        # elapsed time since appearing
            "active": False    # whether message is currently visible
        }

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
                self.spawn_msg["active"] = True
                self.spawn_msg["timer"] = 0
                self.spawn_msg["alpha"] = 0
            else:
                return False  # inactive monsters do nothing
        self.spawn_message_update(dt)

        # Gains extra ground if player is slowed (world scroll slowed)
        if player.colliding:  # slowed
            self.vel = (config.SPEED_NORM - config.SPEED_SLOW) * config.MONSTER_SPEED_DEBUFF * self.buff * -1
        else:
            self.vel = vec(0, 0)

        # Monster moves forward constantly
        self.pos += self.vel * dt

        # Check collision with player
        if aabb(self, player):
            return True

        # Update run animation flipping
        self.time_since_run_flip += dt
        if self.time_since_run_flip >= self.flip_time:
            self.time_since_run_flip = 0
            self.run_frame = 1 - self.run_frame

        return False

    def spawn_message_update(self, dt):
        """Update spawn message timer and alpha"""
        if not self.spawn_msg["active"]:
            return

        self.spawn_msg["timer"] += dt

        # Fade in
        if self.spawn_msg["timer"] < 0.5:
            self.spawn_msg["alpha"] = int((self.spawn_msg["timer"] / 0.5) * 255)
        # Fully visible
        elif self.spawn_msg["timer"] < 3.0:
            self.spawn_msg["alpha"] = 255
        # Fade out
        elif self.spawn_msg["timer"] < 3.5:
            self.spawn_msg["alpha"] = int((1 - (self.spawn_msg["timer"] - 3.0)/0.5) * 255)
        # Done
        else:
            self.spawn_msg["active"] = False