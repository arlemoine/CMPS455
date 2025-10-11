class Ball:
    """Model for Pong ball."""

    def __init__(self, x: int, y: int, bound_top: int, bound_bottom: int, bound_left: int, bound_right: int):
        self.radius = 10
        self.x = x
        self.y = y

        # Hitbox coordinates with buffer for collision detection
        self.hitbox_buffer = 4
        self.hitbox_x1 = 0
        self.hitbox_y1 = 0
        self.hitbox_x2 = 0
        self.hitbox_y2 = 0

        # Ball movement boundaries
        self.MIN_Y = bound_top + self.radius
        self.MAX_Y = bound_bottom - self.radius
        self.MIN_X = bound_left + self.radius
        self.MAX_X = bound_right - self.radius

        # Velocity (pixels/sec)
        self.vx = 200
        self.vy = 30

        # Friction reduces speed each frame; close to 1.0 keeps ball mostly constant
        self.FRICTION_FACTOR = 0.9995
        self.MIN_SPEED = 200

        self.update_hitbox()

    def move(self, dt):
        """Update ball position using velocity and time delta, with Y-bound bounce."""
        # Apply friction
        self.vx *= self.FRICTION_FACTOR
        self.vy *= self.FRICTION_FACTOR

        # Move ball
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Bounce off top/bottom
        if self.y <= self.MIN_Y or self.y >= self.MAX_Y:
            self.y = max(self.MIN_Y, min(self.y, self.MAX_Y))
            self.vy *= -1

        self.update_hitbox()

    def update_hitbox(self):
        """Update rectangular hitbox based on center position and radius."""
        self.hitbox_x1 = self.x - self.radius - self.hitbox_buffer
        self.hitbox_x2 = self.x + self.radius + self.hitbox_buffer
        self.hitbox_y1 = self.y - self.radius - self.hitbox_buffer
        self.hitbox_y2 = self.y + self.radius + self.hitbox_buffer
