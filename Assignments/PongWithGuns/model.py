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
        # Collision check and correction
        if self.collision_check():
            self.ball.vx *= -1
        
        # Paddles
        for paddle_model in self.paddles:
            paddle_model.move(dt)

        for ball in self.balls:
            ball.move(dt)

    def collision_check(self):
        """Check for collision between paddle and ball."""
        # Check against paddle 1
        if (
            self.ball.x <= self.paddle1.hitbox_x2 and 
            self.ball.x >= self.paddle1.hitbox_x1 and
            self.ball.y <= self.paddle1.hitbox_y2 and
            self.ball.y >= self.paddle1.hitbox_y1
        ):
            return True
        # Check against paddle 2
        elif (
            self.ball.x <= self.paddle2.hitbox_x2 and 
            self.ball.x >= self.paddle2.hitbox_x1 and
            self.ball.y <= self.paddle2.hitbox_y2 and
            self.ball.y >= self.paddle2.hitbox_y1
        ):
            return True
        else:
            return False