import pygame as pg
import config
import math
from controller.game_state import GameState

class View:
    """View component for Asteroids."""

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption("Astroids")
        self.font = pg.font.Font(None, 50)

        # Load game banner image (New)
        try:
            # Assuming game_banner.png is in the assets directory
            self.game_banner_img = pg.image.load(config.DIR_ASSETS + "game_banner.png").convert_alpha()
        except pg.error as e:
            print(f"Warning: Could not load game_banner.png. Using placeholder text. Error: {e}")
            self.game_banner_img = None 

        # Load ship image
        ship_img = pg.image.load(config.DIR_ASSETS + "ship01.png").convert_alpha()
        self.ship_img = pg.transform.scale(ship_img, (50, 50))  # scale to size you want

        # Load other assets later (asteroids, bullets, explosions)
        self.bullet_color = config.YELLOW
        self.bullet_radius = 2

    def draw_ship(self, ship):
        """Draw ship rotated at current angle."""
        rotated = pg.transform.rotate(self.ship_img, -ship.angle)  # Pygame rotates counter-clockwise
        rect = rotated.get_rect(center=(ship.x, ship.y))
        self.screen.blit(rotated, rect)

    def draw_bullet(self, bullet):
        pg.draw.circle(self.screen, self.bullet_color, (int(bullet.x), int(bullet.y)), self.bullet_radius)

    def draw_asteroid(self, asteroid):
        pg.draw.circle(self.screen, (150, 150, 150), (int(asteroid.x), int(asteroid.y)), asteroid.radius)

    def draw_particle(self, particle):
        """Draws a single background particle."""
        pg.draw.circle(self.screen, particle.color, 
                       (int(particle.x), int(particle.y)), 
                       particle.radius)

    def draw_text(self, text, x, y, size=50, color=config.WHITE):
        font = pg.font.Font(None, size)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)

    def draw_text_card(self, text, x, y, size=50, text_color=config.BLACK, rect_color=config.SILVER, min_width=0, border_color=None, border_width=0):
        font = pg.font.Font(None, size)
        text_surf = font.render(text, True, text_color)
        
        # 1. Get the Rect of the text for size and positioning
        text_rect = text_surf.get_rect(center=(x, y))

        # 2. Determine the width of the background box
        # Use the requested minimum width or the actual text width, whichever is larger
        required_width = max(text_rect.width, min_width)

        # 3. Create the background rect based on the calculated width
        padding_x = 50
        padding_y = 40
        bkgd_rect = pg.Rect(0, 0, required_width + padding_x, text_rect.height + padding_y)
        bkgd_rect.center = (x, y) # Center the background where the text should be

        # 4. Draw background (filled rectangle)
        pg.draw.rect(self.screen, rect_color, bkgd_rect, border_radius=10)

        # 5. Draw border if specified (must be drawn after the filled rect)
        if border_color and border_width > 0:
            # We use the same rect, but draw it with a specified width (not filled)
            pg.draw.rect(self.screen, border_color, bkgd_rect, border_radius=10, width=border_width)

        # 6. Draw text
        self.screen.blit(text_surf, text_rect)

    def draw_menu(self, controller):
        banner_y = config.SCREEN_HEIGHT // 4
        banner_x = config.SCREEN_WIDTH // 2
        
        rect = self.game_banner_img.get_rect(center=(banner_x, banner_y))
        self.screen.blit(self.game_banner_img, rect)

        x = config.SCREEN_WIDTH // 2
        
        # Shift menu options down slightly to accommodate the banner
        y1 = (config.SCREEN_HEIGHT // 8) * 5 
        y2 = (config.SCREEN_HEIGHT // 8) * 6

        # Fixed width for menu cards
        menu_card_width = 400
        
        rect_color = [config.SILVER] * 2
        border = [0] * 2
        text_color = [config.BLACK] * 2
        
        rect_color[controller.menu_choice] = config.COSMIC_PURPLE
        border[controller.menu_choice] = 3 # Border width for selected item
        text_color[controller.menu_choice] = config.SILVER

        self.draw_text_card("Play", x, y1, text_color=text_color[0], rect_color=rect_color[0], min_width=menu_card_width, border_color=config.VIBRANT_CYAN, border_width=border[0])
        self.draw_text_card("Quit", x, y2, text_color=text_color[1], rect_color=rect_color[1], min_width=menu_card_width, border_color=config.VIBRANT_CYAN, border_width=border[1])

    def render(self, controller, model):
        """Render all game objects."""
        self.screen.fill(config.BLACK)

        if controller.state == GameState.MENU:
            # Draw menu
            for particle in model.particles:
                self.draw_particle(particle)

            self.draw_menu(controller)

        if controller.state == GameState.PLAYING or controller.state == GameState.PAUSED:
            # Draw ship
            self.draw_ship(model.ship)

            # Draw bullets
            for bullet in model.ship.bullets:
                self.draw_bullet(bullet)

            # Draw asteroids
            for asteroid in model.asteroids:
                self.draw_asteroid(asteroid)

            # Optional: draw score, lives, etc.

            if controller.state == GameState.PAUSED:
                self.draw_text_card("PAUSED", (config.SCREEN_WIDTH // 2), (config.SCREEN_HEIGHT // 2))

        pg.display.flip()
