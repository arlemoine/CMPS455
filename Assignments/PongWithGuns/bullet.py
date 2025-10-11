class Bullet:
    """Model for Pong bullet."""

    def __init__(self, x: int, y: int, direction: int, bound_top: int, bound_bottom: int, bound_left: int, bound_right: int):
        """Init instance of game bullet."""
        self.radius = 2
        self.x = x # x coordinate
        self.y = y # y coordinate

        self.hitbox_buffer = 1
        self.hitbox_x1 = 0
        self.hitbox_y1 = 0
        self.hitbox_x2 = 0
        self.hitbox_y2 = 0

        self.MIN_Y = bound_top + self.radius
        self.MAX_Y = bound_bottom - self.radius
        self.MIN_X = bound_left + self.radius
        self.MAX_X = bound_right - self.radius

        self.width = self.radius * 2 # Define for consistency, though not used in movement
        self.MIN_X_REMOVE = bound_left - self.width  # Remove when slightly off-screen left
        self.MAX_X_REMOVE = bound_right + self.width # Remove when slightly off-screen right
        

        self.speed = 600 
        self.vx = self.speed * direction

        self.update_hitbox()

    def move(self, dt):
        """
        Utilize time displacement to determine new location.
        Returns True if the bullet is still active, False if it should be removed.
        """
        
        self.x += self.vx * dt
        
        # Check if the bullet has gone past the side boundaries
        if self.x < self.MIN_X_REMOVE or self.x > self.MAX_X_REMOVE:
            return False  # Bullet is off-screen, remove it

        # Check if the bullet hits vertical boundaries (optional, but good practice)
        # Note: If a paddle shoots a straight bullet, this isn't strictly necessary.
        if self.y <= self.MIN_Y or self.y >= self.MAX_Y:
                # If you want to remove bullets that hit the top/bottom:
                # return False
                # For now, we'll keep it simple and assume the shooter is centered.
                pass

        self.update_hitbox()
        return True # Bullet is still on screen

    def update_hitbox(self):
        """Recalculate all four rectangular hitbox coordinates based on center (x, y) and radius."""
        
        # X-Coordinates: Center +/- Radius +/- Buffer
        self.hitbox_x1 = self.x - self.radius - self.hitbox_buffer
        self.hitbox_x2 = self.x + self.radius + self.hitbox_buffer
        
        # Y-Coordinates: Center +/- Radius +/- Buffer
        self.hitbox_y1 = self.y - self.radius - self.hitbox_buffer
        self.hitbox_y2 = self.y + self.radius + self.hitbox_buffer