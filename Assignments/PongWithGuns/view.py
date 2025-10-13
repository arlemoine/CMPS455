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
        pg.init()
        self.screen = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption("Pong with Guns")
        self.font = pg.font.Font(None, 74)
        
    def draw_start_menu(self):
        self.screen.fill((0, 0, 0))
        font = pg.font.SysFont(None, 48)
        options = [
            "[1] Player vs AI",
            "[2] Player vs Player",
            "[Q] Quit"
        ]
        for i, text in enumerate(options):
            label = font.render(text, True, (255, 255, 255))
            self.screen.blit(label, (self.SCREEN_WIDTH // 2 - label.get_width() // 2,
                                     150 + i * 60))
        pg.display.flip()
    
    def interpolate_color(self, color1, color2, fraction):
        """Blend between two RGB colors."""
        r = int(color1[0] + (color2[0] - color1[0]) * fraction)
        g = int(color1[1] + (color2[1] - color1[1]) * fraction)
        b = int(color1[2] + (color2[2] - color1[2]) * fraction)
        return (r, g, b)
    
    def draw_paddle(self, paddle_model):
        """Draw paddle with color based on height."""
        top_left_x = paddle_model.x - (paddle_model.width // 2)
        top_left_y = paddle_model.y - (paddle_model.height // 2)
        paddle_rect = pg.Rect(top_left_x, top_left_y, paddle_model.width, paddle_model.height)

        # Dynamic color logic based on height
        height_ratio = (paddle_model.height - paddle_model.MIN_HEIGHT) / \
                       (paddle_model.original_height - paddle_model.MIN_HEIGHT)
        height_ratio = max(0, min(1, height_ratio))

        WHITE_THRESHOLD, YELLOW_THRESHOLD, ORANGE_THRESHOLD = 0.75, 0.50, 0.25

        if height_ratio > WHITE_THRESHOLD:
            color = WHITE
        elif height_ratio > YELLOW_THRESHOLD:
            fraction = (height_ratio - YELLOW_THRESHOLD) / (WHITE_THRESHOLD - YELLOW_THRESHOLD)
            color = self.interpolate_color(YELLOW, WHITE, fraction)
        elif height_ratio > ORANGE_THRESHOLD:
            fraction = (height_ratio - ORANGE_THRESHOLD) / (YELLOW_THRESHOLD - ORANGE_THRESHOLD)
            color = self.interpolate_color(ORANGE, YELLOW, fraction)
        else:
            fraction = height_ratio / ORANGE_THRESHOLD
            color = self.interpolate_color(RED, ORANGE, fraction)

        if paddle_model.height <= paddle_model.MIN_HEIGHT:
            color = RED

        pg.draw.rect(self.screen, color, paddle_rect)

    def draw_ball(self, ball_model):
        pg.draw.circle(self.screen, WHITE, (int(ball_model.x), int(ball_model.y)), ball_model.radius)

    def draw_bullet(self, bullet_model):
        pg.draw.circle(self.screen, WHITE, (int(bullet_model.x), int(bullet_model.y)), bullet_model.radius)

    def draw_particle(self, particle_model):
        """Draw fading particle based on lifetime."""
        ratio = 1 - (particle_model.time_elapsed / particle_model.lifetime)
        radius = int(particle_model.radius * ratio)
        if radius > 0:
            pg.draw.circle(self.screen, YELLOW, (int(particle_model.x), int(particle_model.y)), radius)

    def draw_heat_bar(self, model):
        """Draw weapon heat bar for each player."""
        bar_width = self.SCREEN_WIDTH // 3
        bar_height = 12
        margin = 20
        line_thickness = 4

        # Player 1
        p1_ratio = model.p1_heat / model.MAX_HEAT
        p1_x, p1_y = 50, margin
        pg.draw.rect(self.screen, WHITE, (p1_x, p1_y, bar_width, bar_height), 2)
        p1_line_x = p1_x + int(p1_ratio * bar_width)
        color = RED if model.p1_overheated else ORANGE
        pg.draw.line(self.screen, color, (p1_line_x, p1_y), (p1_line_x, p1_y + bar_height), line_thickness)

        # Player 2
        p2_ratio = model.p2_heat / model.MAX_HEAT
        p2_x, p2_y = self.SCREEN_WIDTH - bar_width - 50, margin
        pg.draw.rect(self.screen, WHITE, (p2_x, p2_y, bar_width, bar_height), 2)
        p2_line_x = p2_x + int(p2_ratio * bar_width)
        color = RED if model.p2_overheated else ORANGE
        pg.draw.line(self.screen, color, (p2_line_x, p2_y), (p2_line_x, p2_y + bar_height), line_thickness)

    def draw_text(self, text, x, y, size=74, color=WHITE):
        font = pg.font.Font(None, size)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)

    def draw_score(self, current_score):
        self.draw_text(f"{current_score[0]} : {current_score[1]}", self.SCREEN_WIDTH // 2, 50)

    def render(self, model, current_score, game_running):
        self.screen.fill(BLACK)

        # Draw paddles
        for paddle in [model.paddle1, model.paddle2]:
            self.draw_paddle(paddle)

        if game_running:
            for ball in model.balls:
                self.draw_ball(ball)
            for bullet in model.bullets:
                self.draw_bullet(bullet)
            for particle in model.particles:
                self.draw_particle(particle)

            self.draw_score(current_score)
            self.draw_heat_bar(model)

            # Countdown at 75% down the screen
            if model.round_timer > 0:
                time_left = max(0, int(model.round_timer) + 1)
                self.draw_text(str(time_left), self.SCREEN_WIDTH // 2, (self.SCREEN_HEIGHT * 3) // 4, size=150)

        if not game_running:
            winner = 1 if current_score[0] > current_score[1] else 2
            self.draw_text(f"Player {winner} Wins!", self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2, size=100)
            self.draw_text("Play Again? (Y/N)", self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 100, size=50)

        pg.display.flip()
