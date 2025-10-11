import pygame as pg


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)


class PongView:
    """View component of Pong With Guns."""
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

    def __init__(self):
        """Init pygame window and assets."""
        pg.init()
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption("Pong with Guns")
        self.font = pg.font.Font(None, 74) 
        
    def interpolate_color(self, color1, color2, fraction):
        """Helper to blend between two RGB colors."""
        # Ensure the color blending logic is included here
        r = int(color1[0] + (color2[0] - color1[0]) * fraction)
        g = int(color1[1] + (color2[1] - color1[1]) * fraction)
        b = int(color1[2] + (color2[2] - color1[2]) * fraction)
        return (r, g, b)
    
    def draw_paddle(self, paddle_model):
        """Draw paddle by referencing its state, with color changing based on height."""
        # Calculate the top-left corner needed for pygame.Rect
        top_left_x = paddle_model.x - (paddle_model.width // 2)
        top_left_y = paddle_model.y - (paddle_model.height // 2)
        
        paddle_rect = pg.Rect(top_left_x, top_left_y, paddle_model.width, paddle_model.height)

        # ⭐ NEW: Dynamic Color Logic based on Paddle Height ⭐
        current_color = WHITE # Default
        
        # Calculate the current height as a fraction of the total possible shrinkage
        # 0 = min height, 1 = original height
        height_ratio = (paddle_model.height - paddle_model.MIN_HEIGHT) / \
                       (paddle_model.original_height - paddle_model.MIN_HEIGHT)

        # Clamp the ratio between 0 and 1
        height_ratio = max(0, min(1, height_ratio))

        # Define thresholds for color changes (as fractions of height_ratio)
        WHITE_THRESHOLD = 0.75 # Top 25% of health is white
        YELLOW_THRESHOLD = 0.50 # Between 75% and 50% is yellow gradient
        ORANGE_THRESHOLD = 0.25 # Between 50% and 25% is orange gradient
        # Below 25% (or min height) is red

        if height_ratio > WHITE_THRESHOLD:
            current_color = WHITE
        elif height_ratio > YELLOW_THRESHOLD: # Transition from White to Yellow
            # Scale fraction for this segment: (height_ratio - YELLOW_THRESHOLD) / (WHITE_THRESHOLD - YELLOW_THRESHOLD)
            fraction = (height_ratio - YELLOW_THRESHOLD) / (WHITE_THRESHOLD - YELLOW_THRESHOLD)
            current_color = self.interpolate_color(YELLOW, WHITE, fraction)
        elif height_ratio > ORANGE_THRESHOLD: # Transition from Yellow to Orange
            # Scale fraction for this segment: (height_ratio - ORANGE_THRESHOLD) / (YELLOW_THRESHOLD - ORANGE_THRESHOLD)
            fraction = (height_ratio - ORANGE_THRESHOLD) / (YELLOW_THRESHOLD - ORANGE_THRESHOLD)
            current_color = self.interpolate_color(ORANGE, YELLOW, fraction)
        else: # Below ORANGE_THRESHOLD (including MIN_HEIGHT), transition from Orange to Red, or just Red
            # Scale fraction for this segment: (height_ratio - 0) / (ORANGE_THRESHOLD - 0)
            fraction = (height_ratio - 0) / (ORANGE_THRESHOLD - 0)
            current_color = self.interpolate_color(RED, ORANGE, fraction)
            
        # Ensure it's never too close to black if min_height is 0 and it hits 0.
        if paddle_model.height <= paddle_model.MIN_HEIGHT:
            current_color = RED

        pg.draw.rect(self.screen, current_color, paddle_rect)

    def draw_ball(self, ball_model):
        """Draw ball by referencing its state."""
        pg.draw.circle(
            self.screen, 
            WHITE, 
            (int(ball_model.x), int(ball_model.y)), # Center (x, y) - casting to int is safer
            ball_model.radius
        )

    def draw_bullet(self, bullet_model):
        """Draw bullet by referencing its state."""
        pg.draw.circle(
            self.screen, 
            WHITE, 
            (int(bullet_model.x), int(bullet_model.y)), 
            bullet_model.radius
        )

    def draw_particle(self, particle_model):
        """Draws the temporary particle."""
        # Calculate size reduction based on remaining lifespan for a "fading" effect
        ratio = 1 - (particle_model.time_elapsed / particle_model.lifetime)
        current_radius = int(particle_model.radius * ratio)
        
        # Only draw if it's still visible
        if current_radius > 0:
            pg.draw.circle(
                self.screen, 
                YELLOW, 
                (int(particle_model.x), int(particle_model.y)), 
                current_radius
            )

    def draw_heat_bar(self, model):
        """Draws a thin line showing weapon overheat for each player."""
        bar_width = self.SCREEN_WIDTH // 3
        bar_height = 12   # thin bar
        margin = 20       # padding from top
        line_thickness = 4

        # --- Player 1 heat bar (left) ---
        p1_ratio = model.p1_heat / model.MAX_HEAT  # 0.0 → 1.0
        p1_bar_x = 50
        p1_bar_y = margin

        # Outer transparent bar outline
        pg.draw.rect(self.screen, WHITE, (p1_bar_x, p1_bar_y, bar_width, bar_height), width=2)

        # Moving line to show heat
        p1_line_x = p1_bar_x + int(p1_ratio * bar_width)
        heat_color = ORANGE if not model.p1_overheated else RED
        pg.draw.line(self.screen, heat_color,
                    (p1_line_x, p1_bar_y),
                    (p1_line_x, p1_bar_y + bar_height),
                    line_thickness)

        # --- Player 2 heat bar (right) ---
        p2_ratio = model.p2_heat / model.MAX_HEAT
        p2_bar_x = self.SCREEN_WIDTH - bar_width - 50
        p2_bar_y = margin

        pg.draw.rect(self.screen, WHITE, (p2_bar_x, p2_bar_y, bar_width, bar_height), width=2)

        p2_line_x = p2_bar_x + int(p2_ratio * bar_width)
        heat_color = ORANGE if not model.p2_overheated else RED
        pg.draw.line(self.screen, heat_color,
                    (p2_line_x, p2_bar_y),
                    (p2_line_x, p2_bar_y + bar_height),
                    line_thickness)


    def draw_text(self, text, x, y, size=74, color=WHITE):
        """Helper function to draw text on the screen."""
        font = pg.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_score(self, current_score):
        """Draw the current score of both players."""
        screen_center_x = self.SCREEN_WIDTH // 2
        # Use the helper to draw the score
        score_text = f"{current_score[0]} : {current_score[1]}"
        self.draw_text(score_text, screen_center_x, 50) 

    def render(self, model, current_score, game_running): 
        self.screen.fill(BLACK)

        # Draw paddles and balls and bullets
        for paddle_model in [model.paddle1, model.paddle2]:
            self.draw_paddle(paddle_model)

        if game_running:
            for ball in model.balls:
                self.draw_ball(ball)

            for bullet in model.bullets:
                self.draw_bullet(bullet)

            for particle in model.particles:
                self.draw_particle(particle)
        
        # Draw the score
        if game_running:
            self.draw_score(current_score) 

            self.draw_heat_bar(model)

            # DRAW COUNTDOWN TEXT
            if model.round_timer > 0:
                time_left = max(0, int(model.round_timer) + 1)
                self.draw_text(str(time_left), 
                    (self.SCREEN_WIDTH // 2),   # X = center horizontally
                    ((self.SCREEN_HEIGHT // 4) * 3),  # Y = center vertically
                    size=150)

        # Draw Game Over screen using game_running status
        if not game_running:
            # Determine winner logic here (based on current_score)
            winner_index = 0 if current_score[0] > current_score[1] else 1
            winner = winner_index + 1
            self.draw_text(f"Player {winner} Wins!", self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, size=100)
            self.draw_text("Play Again? (Y/N)", self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 100, size=50)

        pg.display.flip()