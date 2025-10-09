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

    def render(self, model):
        self.screen.fill(BLACK)

        # Draw paddles
        for paddle_model in model.paddles:
            self.draw_paddle(paddle_model)

        # Draw balls
        for ball in model.balls:
            self.draw_ball(ball)

        pg.display.flip()