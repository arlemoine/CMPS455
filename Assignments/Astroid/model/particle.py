import math
import random

import config

class Particle:
    """Represents a single shooting star particle for the background."""

    def __init__(self):      
        # Introduce randomness to the speed 
        speed_multiplier = random.uniform(0.5, 1.5)
        self.speed = config.PARTICLE_SPEED * speed_multiplier
        
        # Choose to spawn on the Top Edge or the Right Edge
        if random.choice([True, False]):
            # Spawn on the Top Edge (Right 75% segment)
            # X is between 25% and 100% of the screen width
            x_min = config.HARD_BOUNDARY_RIGHT * 0.25 
            x_max = config.HARD_BOUNDARY_RIGHT
            
            self.x = random.uniform(x_min, x_max)
            # Y is just above the top boundary to appear to enter
            self.y = config.HARD_BOUNDARY_TOP - 1 
        else:
            # Spawn on the Right Edge (Top 75% segment)
            # Y is between 0% and 75% of the screen height
            y_min = config.HARD_BOUNDARY_TOP
            y_max = config.HARD_BOUNDARY_BOTTOM * 0.75 
            
            # X is just outside the right boundary
            self.x = config.HARD_BOUNDARY_RIGHT + 1 
            self.y = random.uniform(y_min, y_max)
        
        # Fixed Diagonal Velocity (Top-Right to Bottom-Left)
        
        # The base vector is (-1, 1) for Left (negative x) and Down (positive y).
        vx_component = -1
        vy_component = 1
        
        # Normalize the vector to maintain constant speed on the diagonal
        magnitude = math.hypot(vx_component, vy_component)
        
        # Calculate final velocity components using the randomized speed
        self.vx = (vx_component / magnitude) * self.speed
        self.vy = (vy_component / magnitude) * self.speed
        
        self.expired = False
        
        # Visuals
        self.color = random.choice([config.SILVER, config.YELLOW])
        self.radius = max(1, min(4, int(1 + speed_multiplier * 1.5)))

    def update(self, dt):
        """Move the particle and check for expiration."""
        self.x += self.vx * dt
        self.y += self.vy * dt

        self._check_expiration()

    def _check_expiration(self):
        """Check if the particle has moved off the bottom or left edge."""
        # Expires if it moves off the left edge (x < HARD_BOUNDARY_LEFT) 
        # OR off the bottom edge (y > HARD_BOUNDARY_BOTTOM)
        if self.x < config.HARD_BOUNDARY_LEFT or self.y > config.HARD_BOUNDARY_BOTTOM:
            self.expired = True
            
