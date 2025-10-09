

class Ball:
    """Model for Pong ball."""

    def __init__(self, x: int, y: int, bound_top: int, bound_bottom: int, bound_left: int, bound_right: int):
        """Init instance of game paddle."""
        self.radius = 10
        self.x = x # x coordinate
        self.y = y # y coordinate

        self.hitbox_buffer = 4
        self.hitbox_x1 = 0
        self.hitbox_y1 = 0
        self.hitbox_x2 = 0
        self.hitbox_y2 = 0

        self.MIN_Y = bound_top + self.radius
        self.MAX_Y = bound_bottom - self.radius
        self.MIN_X = bound_left + self.radius
        self.MAX_X = bound_right - self.radius

        self.vx = 200
        self.vy = 5

        self.update_hitbox()

    def move(self, dt):
        """Utilize direction and time displacement to determine new location."""
        self.x += self.vx * dt
        self.y += self.vy * dt

        if (
            self.x <= self.MIN_X or 
            self.x >= self.MAX_X
        ):
            self.x = max(self.MIN_X, min(self.x, self.MAX_X)) 
            self.vx *= -1
        if (
            self.y <= self.MIN_Y or 
            self.y >= self.MAX_Y
        ):
            self.y = max(self.MIN_Y, min(self.y, self.MAX_Y))
            self.vy *= -1

        self.update_hitbox()

    def update_hitbox(self):
        """Recalculate all four rectangular hitbox coordinates based on center (x, y) and radius."""
        
        # X-Coordinates: Center +/- Radius +/- Buffer
        self.hitbox_x1 = self.x - self.radius - self.hitbox_buffer
        self.hitbox_x2 = self.x + self.radius + self.hitbox_buffer
        
        # Y-Coordinates: Center +/- Radius +/- Buffer
        self.hitbox_y1 = self.y - self.radius - self.hitbox_buffer
        self.hitbox_y2 = self.y + self.radius + self.hitbox_buffer

    def reflect_vector(self, normal_x: float, normal_y: float):
        """Calculates and sets the new velocity vector based on the surface normal."""
        
        # Current velocity vector V: (self.vx, self.vy)
        # Normal vector N: (normal_x, normal_y)

        # 1. Normalize the normal vector (ensure magnitude is 1)
        # Assuming the caller provides a normalized normal (e.g., (1, 0) or (-1, 0)) for simplicity.
        
        # 2. Calculate the projection of V onto N (V dot N)
        dot_product = self.vx * normal_x + self.vy * normal_y
        
        # 3. Calculate the reflected vector R = V - 2 * (V dot N) * N
        self.vx -= 2 * dot_product * normal_x
        self.vy -= 2 * dot_product * normal_y