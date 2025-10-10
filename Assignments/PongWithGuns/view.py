import pygame as pg


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class PongView:
    """View component of Pong With Guns."""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    def __init__(self):
        """Init pygame window and assets."""
        pg.init()
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption("Pong with Guns")
        self.font = pg.font.Font(None, 74) 
        
    def draw_paddle(self, paddle_model):
        """Draw paddle by referencing its state."""
        # Calculate the top-left corner needed for pygame.Rect
        top_left_x = paddle_model.x - (paddle_model.width // 2)
        top_left_y = paddle_model.y - (paddle_model.height // 2)
        
        paddle_rect = pg.Rect(top_left_x, top_left_y, paddle_model.width, paddle_model.height)
        pg.draw.rect(self.screen, WHITE, paddle_rect)

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

        for ball in model.balls:
            self.draw_ball(ball)

        for bullet in model.bullets:
            self.draw_bullet(bullet)
        
        # Draw the score
        self.draw_score(current_score) 

        # DRAW COUNTDOWN TEXT
        if model.round_timer > 0:
            time_left = max(0, int(model.round_timer) + 1)
            self.draw_text(str(time_left), 
                           self.SCREEN_WIDTH // 2, 
                           self.SCREEN_HEIGHT // 2, 
                           size=150)

        # Draw Game Over screen using game_running status
        if not game_running:
            # Determine winner logic here (based on current_score)
            winner_index = 0 if current_score[0] > current_score[1] else 1
            winner = winner_index + 1
            self.draw_text(f"Player {winner} Wins!", self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, size=100)
            self.draw_text("Play Again? (Y/N)", self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 100, size=50)

        pg.display.flip()