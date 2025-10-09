from paddle import Paddle
from ball import Ball


class PongModel:
    """Model for Pong With Guns."""

    def __init__(self, screen_width, screen_height):
        """Init instance of game model."""
        # Store screen dimensions for boundary logic
        self.width = screen_width
        self.height = screen_height

        BOUNDARY_TOP = 0
        BOUNDARY_BOTTOM = self.height       
        BOUNDARY_LEFT = 0
        BOUNDARY_RIGHT = self.width 

        self.paddle1 = Paddle(50, self.height // 2, BOUNDARY_TOP, BOUNDARY_BOTTOM) # Left paddle
        self.paddle2 = Paddle(self.width - 60, self.height // 2, BOUNDARY_TOP, BOUNDARY_BOTTOM) # Right paddle
        self.paddles = [self.paddle1, self.paddle2]

        self.ball = Ball(self.width // 2, self.height // 2, BOUNDARY_TOP, BOUNDARY_BOTTOM, BOUNDARY_LEFT, BOUNDARY_RIGHT)
        self.balls = [self.ball]

        self.score=[0,0]

    def update(self, dt): 
        """Update position and state of all game objects."""      
        # Paddles
        for paddle_model in self.paddles:
            paddle_model.move(dt)

        for ball in self.balls:
            ball.move(dt)

        self.collision_check()

    def collision_check(self):
        """Check for collision and handle bounce using reflection."""
        
        # Check against paddle 1 (Left Paddle)
        if (
            (self.ball.hitbox_x2) >= self.paddle1.hitbox_x1 and 
            self.ball.hitbox_x1 <= self.paddle1.hitbox_x2 and
            self.ball.hitbox_y2 >= self.paddle1.hitbox_y1 and # Use ball's full hitbox
            self.ball.hitbox_y1 <= self.paddle1.hitbox_y2 
        ):
            # Ball hit Paddle 1. Normal for left paddle points RIGHT (1, 0)
            normal_x, normal_y = self.paddle1.get_normal(is_left_paddle=True)
            self.ball.reflect_vector(normal_x, normal_y)
            return True # Not strictly needed if logic is in update, but good for clarity
            
        # Check against paddle 2 (Right Paddle)
        elif (
            self.ball.hitbox_x2 >= self.paddle2.hitbox_x1 and 
            self.ball.hitbox_x1 <= self.paddle2.hitbox_x2 and
            self.ball.hitbox_y2 >= self.paddle2.hitbox_y1 and 
            self.ball.hitbox_y1 <= self.paddle2.hitbox_y2
        ):
            # Ball hit Paddle 2. Normal for right paddle points LEFT (-1, 0)
            normal_x, normal_y = self.paddle2.get_normal(is_left_paddle=False)
            self.ball.reflect_vector(normal_x, normal_y)
            return True
        
        return False