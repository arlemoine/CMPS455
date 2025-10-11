
class Particle:
    """Model for a brief visual effect particle."""

    def __init__(self, x, y, lifetime=0.15, size=3):
        """Initializes a particle at (x, y) with a short lifespan."""
        self.x = x
        self.y = y
        self.radius = size
        self.lifetime = lifetime  # Max time the particle will exist (seconds)
        self.time_elapsed = 0.0

    def update(self, dt):
        """Updates the particle's lifespan. Returns True if alive, False if expired."""
        self.time_elapsed += dt
        
        # We don't need movement (vx/vy) for a simple sparkle, just lifespan.
        
        return self.time_elapsed < self.lifetime