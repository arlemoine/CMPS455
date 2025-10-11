

class Paddle:
    """Model for Pong paddle."""

    def __init__(self, x: int, y: int, bound_top: int, bound_bottom: int):
        """Init instance of game paddle."""
        self.x = x # x coordinate
        self.y = y # y coordinate
        self.width = 10
        self.height = 80
        self.original_height = self.height
        self.MIN_Y = bound_top + (self.height // 2)
        self.MAX_Y = bound_bottom - (self.height // 2)
        self.hitbox_buffer = 10 # Pixel buffer
        self.hitbox_x1 = self.x - self.hitbox_buffer
        self.hitbox_y1 = self.y - self.hitbox_buffer
        self.hitbox_x2 = self.hitbox_x1 + self.width + (2 * self.hitbox_buffer)
        self.hitbox_y2 = self.hitbox_y1 + self.height + (2 * self.hitbox_buffer)

        self.base_speed = 240
        self.speed = self.base_speed
        self.direction = 0

        # Growth/shrink properties
        self.MIN_HEIGHT = 14  # Minimum size it can shrink to
        self.SHRINK_AMOUNT = 8 # Amount to shrink per hit
        self.GROWTH_RATE = 2.0 # Pixels per second to grow back

    def set_direction(self, direction: int = 0):
        self.direction = direction

    def move(self, dt):
        """Utilize direction and time displacement to determine new location."""
        self.y = self.y + (self.speed * self.direction * dt)
        self.y = max(self.MIN_Y, min(self.y, self.MAX_Y))
        self.update_hitbox()

    def update_hitbox(self):
        half_height = self.height // 2
        
        # X-Coordinates (no change, as x was already treated as center x for a vertical paddle)
        self.hitbox_x1 = self.x - self.hitbox_buffer
        self.hitbox_x2 = self.hitbox_x1 + self.width + (2 * self.hitbox_buffer)
        
        # Y-Coordinates (start from the center, subtract half height + buffer)
        self.hitbox_y1 = self.y - half_height - self.hitbox_buffer
        self.hitbox_y2 = self.y + half_height + self.hitbox_buffer

    def update_size(self, dt):
        """Allows the paddle to grow back to its original size over time."""
        if self.height < self.original_height:
            self.height += self.GROWTH_RATE * dt
            self.speed = self.base_speed * (self.height / self.original_height)
            # Ensure it doesn't overshoot the original height
            if self.height > self.original_height:
                self.height = self.original_height
                self.speed = self.base_speed * (self.height / self.original_height)

    def shrink_on_hit(self):
        """Reduces the paddle's height and recalculates the hitbox."""
        self.height -= self.SHRINK_AMOUNT
        self.speed = self.base_speed * (self.height / self.original_height)
        
        # Ensure the paddle doesn't shrink below the minimum
        if self.height < self.MIN_HEIGHT:
            self.height = self.MIN_HEIGHT

        self.update_hitbox()
