from paddle import Paddle
from ball import Ball
import random


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

        self.bullets = []

        self.SHOOT_RATE = .1 # Time (seconds) between shots
        self.p1_last_shot_time = 0.0
        self.p2_last_shot_time = 0.0

        self.MAX_BOUNCE_SPEED_Y = 300 # Define the speed attribute
        self.MAX_BOUNCE_ANGLE = 75    # Define the angle attribute (not strictly needed but good to keep)

        self.ROUND_DELAY = 1.5 # 1.5 second delay
        self.round_timer = self.ROUND_DELAY # Tracks time elapsed since reset

        self.next_direction_x = random.choice([-1, 1]) 

    def update(self, dt): 
        """Update position and state of all game objects.""" 
        
        # ⭐ REMOVE THIS CALL: self.check_score() ⭐
        
        if self.round_timer > 0:
            self.round_timer -= dt
            
            if self.round_timer <= 0:
                # ⭐ FIX: USE next_direction_x TO SET VX ⭐
                direction_x = self.next_direction_x
                
                # Launch the ball!
                self.ball.vx = self.MAX_BOUNCE_SPEED_Y * direction_x 
                
                # Randomize VY direction and magnitude (same as before)
                random_y_factor = random.uniform(0.2, 1.0) * random.choice([-1, 1])
                self.ball.vy = self.MAX_BOUNCE_SPEED_Y * 0.5 * random_y_factor 
                
        # Only run physics/collision/scoring if the timer has expired
        if self.round_timer <= 0:
            
            # 1. Collision and AI logic (must run before movement)
            self.collision_check()
            self.update_ai_paddle()
            
            # 2. Movement
            for paddle_model in self.paddles:
                paddle_model.move(dt)

            for ball in self.balls:
                ball.move(dt)

            active_bullets = []
            for bullet in self.bullets:
                if bullet.move(dt):
                    active_bullets.append(bullet)
            self.bullets = active_bullets

            # 3. ⭐ CHECK SCORE LAST: Ensures collision is processed before scoring boundary ⭐
            self.check_score() 

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

            ball.vx = abs(ball.vx) * 1.05 # Speed increase

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

    def update_ai_paddle(self):
        """AI logic for controlling the right paddle (self.paddle2)."""
        ball_x = self.ball.x
        paddle2 = self.paddle2
        
        # Determine the target Y position based on the ball's horizontal position
        if ball_x > self.width // 2:
            target_y = self.ball.y
        else:
            target_y = self.paddle1.y
        
        # Calculate movement based on the chosen target Y
        paddle2_y = paddle2.y
        TOLERANCE = 10 

        if paddle2_y < target_y - TOLERANCE:
            paddle2.set_direction(1) # Move down
        
        elif paddle2_y > target_y + TOLERANCE:
            paddle2.set_direction(-1) # Move up
            
        else:
            paddle2.set_direction(0) # Stop

    def check_score(self):
        """
        Checks if the ball has gone past the left or right boundaries.
        Returns 0 if no score, 1 if Player 1 scores, or 2 if Player 2 scores.
        """
        ball = self.ball
        
        # Ball passed LEFT side (Score for Player 2)
        if ball.x < 0: 
            return 2
        
        # Ball passed RIGHT side (Score for Player 1)
        elif ball.x > self.width:
            return 1
            
        return 0 # No score

    # model.py (in PongModel class)

    def reset_ball(self, direction_x):
        """Resets the ball to the center and sets its initial direction."""
        # Reset position to center
        self.ball.x = self.width // 2
        self.ball.y = self.height // 2

        # Reset timer and halt movement temporarily
        self.round_timer = self.ROUND_DELAY
        self.ball.vx = 0
        self.ball.vy = 0

        self.next_direction_x = direction_x
        
    def fire_bullet(self, player_id, current_time):
        """Creates a bullet if the shoot limit allows it."""
        from bullet import Bullet
        
        # ⭐ FIX: Determine which player's timer to use ⭐
        if player_id == 1:
            last_shot = self.p1_last_shot_time
        else: # player_id == 2
            last_shot = self.p2_last_shot_time

        # Check if the player can shoot yet
        if current_time - last_shot < self.SHOOT_RATE:
            return False

        # --- Launch Logic (Remains the same) ---
        paddle = self.paddle1 if player_id == 1 else self.paddle2
        
        direction = 1 if player_id == 1 else -1
        
        offset = paddle.width // 2 + 5
        start_x = paddle.x + (offset * direction)
        start_y = paddle.y
        
        new_bullet = Bullet(start_x, start_y, direction, 
                            0, self.height, 0, self.width) 
                            
        self.bullets.append(new_bullet)
        
        # ⭐ FIX: Reset the correct player's timer ⭐
        if player_id == 1:
            self.p1_last_shot_time = current_time
        else:
            self.p2_last_shot_time = current_time
            
        return True

    def update_ai_shooting(self, current_time):
        """AI (P2) decides whether to shoot based on the ball's position and velocity."""
        
        ball_x = self.ball.x
        
        # AI Shoots if:
        # 1. The ball is on Player 1's side (left half).
        # 2. The ball is moving toward the AI's paddle (vx is negative).
        # This prevents the AI from shooting when the ball is moving away.
        
        if ball_x < self.width // 2 and self.ball.vx < 0:
            # Attempt to fire a bullet (Player 2 is the AI)
            self.fire_bullet(2, current_time)