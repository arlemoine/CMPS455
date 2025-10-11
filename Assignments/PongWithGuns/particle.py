class Particle:
    """Brief visual effect particle."""

    def __init__(self, x, y, lifetime=0.15, size=3):
        self.x = x
        self.y = y
        self.radius = size
        self.lifetime = lifetime  # seconds
        self.time_elapsed = 0.0

    def update(self, dt):
        """Increment lifespan; return True if still alive."""
        self.time_elapsed += dt
        return self.time_elapsed < self.lifetime
