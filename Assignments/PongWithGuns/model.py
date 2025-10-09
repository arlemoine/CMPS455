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
        
        self.MAX_BOUNCE_SPEED_Y = 300 # Define the speed attribute
        self.MAX_BOUNCE_ANGLE = 75    # Define the angle attribute (not strictly needed but good to keep)

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
        """Check for collision and handle angle-based bounce."""
        ball = self.ball

        # We removed the handle_bounce function and put its logic inside the if/elif blocks.

        # Check against paddle 1 (Left Paddle)
        if (
            (ball.hitbox_x2) >= self.paddle1.hitbox_x1 and 
            ball.hitbox_x1 <= self.paddle1.hitbox_x2 and
            ball.hitbox_y2 >= self.paddle1.hitbox_y1 and 
            ball.hitbox_y1 <= self.paddle1.hitbox_y2 
        ):
            paddle = self.paddle1
            relative_y = ball.y - paddle.y
            normalized_y = relative_y / (paddle.height / 2)

            # Use self.MAX_BOUNCE_SPEED_Y
            ball.vy = normalized_y * self.MAX_BOUNCE_SPEED_Y 
            ball.vx *= -1
            ball.vx *= 1.05 # Speed increase
            return True

        # Check against paddle 2 (Right Paddle)
        elif (
            ball.hitbox_x2 >= self.paddle2.hitbox_x1 and 
            ball.hitbox_x1 <= self.paddle2.hitbox_x2 and
            ball.hitbox_y2 >= self.paddle2.hitbox_y1 and 
            ball.hitbox_y1 <= self.paddle2.hitbox_y2
        ):
            paddle = self.paddle2
            relative_y = ball.y - paddle.y
            normalized_y = relative_y / (paddle.height / 2)

            # Use self.MAX_BOUNCE_SPEED_Y
            ball.vy = normalized_y * self.MAX_BOUNCE_SPEED_Y
            ball.vx *= -1
            ball.vx *= 1.05 # Speed increase

            # Ensure the ball moves left after hitting the right paddle
            if ball.vx > 0:
                ball.vx *= -1 

            return True

        return False
