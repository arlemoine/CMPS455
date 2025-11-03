import pygame as pg
import config
import math
from controller.game_state import GameState

class View:
    """View component for astroids."""

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

        self.astroid_images = []
        for i in range(1, 5):
            path = config.DIR_ASSETS + f"astroid_0{i}.png"
            try:
                img = pg.image.load(path).convert_alpha()
                self.astroid_images.append(img)
            except pg.error as e:
                print(f"Warning: Could not load {path}: {e}")

        # Load other assets later (astroids, bullets, explosions)
        self.bullet_color = config.YELLOW
        self.bullet_radius = 2

    def draw_ship(self, ship):
        """Draw ship rotated at current angle."""
        rotated = pg.transform.rotate(self.ship_img, -ship.angle)  # Pygame rotates counter-clockwise
        rect = rotated.get_rect(center=(ship.x, ship.y))
        self.screen.blit(rotated, rect)

    def draw_forcefield(self, forcefield):
        # Determine base color and width based on health
        health_ratio = forcefield.health / forcefield.max_health
        
        # Color transition (e.g., from blue to red when damaged)
        # Interpolate between a healthy color and a danger color
        healthy_color = (0, 150, 255)  # Bright Blue
        danger_color = (255, 50, 0)    # Orange/Red
        
        r = int(healthy_color[0] + (danger_color[0] - healthy_color[0]) * (1 - health_ratio))
        g = int(healthy_color[1] + (danger_color[1] - healthy_color[1]) * (1 - health_ratio))
        b = int(healthy_color[2] + (danger_color[2] - healthy_color[2]) * (1 - health_ratio))
        color = (r, g, b)

        # Use glow_state for alpha (transparency)
        # Map glow_state (e.g., 2-15) to an alpha value (0-255).
        # We cap the alpha to 200 for visibility and scale the glow range.
        # Max alpha: 200 (for high glow)
        # Min alpha: 50 (for low glow)
        
        # Calculate alpha based on glow_state
        glow_range = forcefield.max_glow - forcefield.min_glow
        # Normalize glow_state (0 to 1)
        normalized_glow = (forcefield.glow_state - forcefield.min_glow) / glow_range
        # Map normalized value to the desired alpha range (e.g., 50 to 200)
        alpha_min = 50
        alpha_max = 200
        alpha = int(alpha_min + (alpha_max - alpha_min) * normalized_glow)
        alpha = min(255, max(0, alpha)) # Clamp for safety

        # 1. Create a temporary Surface for drawing the transparent circle
        # The surface size must be large enough for the circle
        surface_size = (forcefield.radius * 2 + 10, forcefield.radius * 2 + 10)
        temp_surface = pg.Surface(surface_size, pg.SRCALPHA) # Use SRCALPHA flag for transparency
        temp_surface.fill((0, 0, 0, 0)) # Fill with transparent black
        
        # 2. Draw the forcefield outline on the temporary Surface
        center = (surface_size[0] // 2, surface_size[1] // 2)
        
        # Draw the main shield (e.g., a thick outline)
        pg.draw.circle(temp_surface, 
                       color + (alpha,), # Combine RGB color with Alpha
                       center, 
                       forcefield.radius, 
                       width=3) # Adjust width for desired effect

        # 3. Blit the temporary surface to the main screen
        # Position the temp_surface so its center aligns with the ship's position
        rect = temp_surface.get_rect(center=(forcefield.x, forcefield.y))
        self.screen.blit(temp_surface, rect)

    def draw_bullet(self, bullet):
        pg.draw.circle(self.screen, self.bullet_color, (int(bullet.x), int(bullet.y)), self.bullet_radius)

    def draw_astroid(self, astroid):
        """Draw an astroid rotated and centered at its position."""
        img = self.astroid_images[astroid.sprite_index]

        # Scale based on astroid size (optional)
        size_scale = astroid.radius * 2
        img = pg.transform.scale(img, (size_scale, size_scale))

        # Apply rotation
        rotated = pg.transform.rotate(img, -astroid.angle)
        rect = rotated.get_rect(center=(astroid.x, astroid.y))

        self.screen.blit(rotated, rect)

    def draw_explosion(self, explosion):
        """Draws an Explosion object with concentric rings that touch each other."""
        num_rings = explosion.num_rings
        ring_radius = explosion.radius
        colors = explosion.rings  # innermost first
        ring_width = 6  # thickness of each ring

        # Maximum radius to hold all rings
        final_radius = ring_radius + ring_width * num_rings
        surface_size = final_radius * 2
        temp_surface = pg.Surface((surface_size, surface_size), pg.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))  # transparent

        center = surface_size // 2

        current_radius = ring_radius + ring_width // 2  # start at inner radius + half width
        for i in range(num_rings):
            color = colors[i]

            alpha = 255
            if hasattr(explosion, "alpha_fade"):
                alpha = int(255 * explosion.alpha_fade)
            color_with_alpha = color + (alpha,)

            pg.draw.circle(
                temp_surface,
                color_with_alpha,
                (center, center),
                current_radius,
                width=ring_width
            )

            # Increment radius by width so next ring touches this one
            current_radius += ring_width

        rect = temp_surface.get_rect(center=(int(explosion.x), int(explosion.y)))
        self.screen.blit(temp_surface, rect)



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
        
        rect_color[controller.menu_choice_index] = config.COSMIC_PURPLE
        border[controller.menu_choice_index] = 3 # Border width for selected item
        text_color[controller.menu_choice_index] = config.SILVER

        self.draw_text_card("Play", x, y1, text_color=text_color[0], rect_color=rect_color[0], min_width=menu_card_width, border_color=config.VIBRANT_CYAN, border_width=border[0])
        self.draw_text_card("Quit", x, y2, text_color=text_color[1], rect_color=rect_color[1], min_width=menu_card_width, border_color=config.VIBRANT_CYAN, border_width=border[1])

    def draw_gameover_menu(self, controller):
        """Draw the Game Over menu on top of the gameplay screen."""
        # Semi-transparent overlay
        overlay = pg.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # "GAME OVER" text
        self.draw_text(
            "GAME OVER",
            config.SCREEN_WIDTH // 2,
            config.SCREEN_HEIGHT // 3,
            size=80,
            color=config.ORANGE
        )

        # Draw menu options (like Continue / Quit)
        x = config.SCREEN_WIDTH // 2
        y_start = config.SCREEN_HEIGHT // 2
        spacing = 100

        options = controller.menus["gameover"]
        for i, label in options.items():
            selected = (i == controller.menu_choice_index)
            rect_color = config.COSMIC_PURPLE if selected else config.SILVER
            text_color = config.SILVER if selected else config.BLACK
            border_color = config.VIBRANT_CYAN if selected else None
            border_width = 3 if selected else 0

            self.draw_text_card(
                label,
                x,
                y_start + i * spacing,
                text_color=text_color,
                rect_color=rect_color,
                min_width=400,
                border_color=border_color,
                border_width=border_width
            )

    # view.py
    def draw_hud(self, model):
        """Draws the HUD at the bottom of the screen (score, level, etc.)."""
        # Background bar
        hud_rect = pg.Rect(
            0,
            config.SCREEN_HEIGHT - config.HUD_HEIGHT,
            config.SCREEN_WIDTH,
            config.HUD_HEIGHT
        )
        pg.draw.rect(self.screen, config.SILVER, hud_rect)

        # Text positions
        hud_y_center = config.SCREEN_HEIGHT - config.HUD_HEIGHT // 2

        # Score (centered)
        score_text = f"Score: {model.score}"
        self.draw_text(
            score_text,
            config.SCREEN_WIDTH // 2,
            hud_y_center,
            size=40,
            color=config.BLACK  # contrast with silver background
        )

        # Level / difficulty (left-aligned in HUD)
        level_text = f"Level: {model.level}"
        self.draw_text(
            level_text,
            20,  # small left padding
            hud_y_center,
            size=30,
            color=config.BLACK  # subtle and readable
        )



    def render(self, controller, model):
        """Render all game objects."""
        self.screen.fill(config.BLACK)

        if controller.state == GameState.MENU:
            # Draw menu
            for particle in model.particles:
                self.draw_particle(particle)

            self.draw_menu(controller)

        if controller.state in (GameState.PLAYING, GameState.PAUSED, GameState.GAMEOVER):
            # Draw explosions first so they are under other objects
            for explosion in model.explosions:
                self.draw_explosion(explosion)
            
            # Draw ship and forcefield (top layer)
            if model.ship.alive:
                if model.ship.forcefield.health > 0:
                    self.draw_forcefield(model.ship.forcefield)
                self.draw_ship(model.ship)

            # Draw bullets
            for bullet in model.ship.bullets:
                self.draw_bullet(bullet)

            # Draw asteroids
            for astroid in model.astroids:
                self.draw_astroid(astroid)

            # Optional: draw score, lives, etc.

            if controller.state == GameState.PAUSED:
                self.draw_text_card("PAUSED", (config.SCREEN_WIDTH // 2), (config.SCREEN_HEIGHT // 2))

            if controller.state == GameState.GAMEOVER:
                self.draw_gameover_menu(controller)

            self.draw_hud(model)

        pg.display.flip()
