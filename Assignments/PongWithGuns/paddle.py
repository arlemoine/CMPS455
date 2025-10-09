

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

    def get_normal(self, is_left_paddle: bool):
        """Returns the normal vector (x, y) for the paddle's impact surface."""
        # Left paddle (hits right face) has a normal pointing LEFT (-1, 0)
        # Right paddle (hits left face) has a normal pointing RIGHT (1, 0)
        
        # The collision logic should be written to ensure the ball is only hitting the face.
        if is_left_paddle:
            return (1, 0)  # Normal points right
        else:
            return (-1, 0) # Normal points left