

class Paddle:
    """Model for Pong paddle."""

    def __init__(self, x: int, y: int, bound_top: int, bound_bottom: int):
        """Init instance of game paddle."""
        self.x = x # x coordinate
        self.y = y # y coordinate
        self.width = 10
        self.height = 60
        self.MIN_Y = bound_top + (self.height // 2)
        self.MAX_Y = bound_bottom - (self.height // 2)
        self.hitbox_buffer = 10 # Pixel buffer
        self.hitbox_x1 = self.x - self.hitbox_buffer
        self.hitbox_y1 = self.y - self.hitbox_buffer
        self.hitbox_x2 = self.hitbox_x1 + self.width + (2 * self.hitbox_buffer)
        self.hitbox_y2 = self.hitbox_y1 + self.height + (2 * self.hitbox_buffer)

        self.speed = 300
        self.direction = 0



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