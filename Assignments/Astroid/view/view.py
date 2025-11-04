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

        # Load game banner
        self.game_banner_img = pg.image.load(config.DIR_ASSETS + "game_banner.png").convert_alpha()

        # Load ship image
        ship_img = pg.image.load(config.DIR_ASSETS + "ship01.png").convert_alpha()
        self.ship_img = pg.transform.scale(ship_img, (50, 50))

        # Load HUD background image
        hud_bkgd_img = pg.image.load(config.DIR_ASSETS + "hud_bkgd.png").convert()
        self.hud_bkgd_img = pg.transform.scale(hud_bkgd_img, (config.SCREEN_WIDTH, config.HUD_HEIGHT))

        self.astroid_images = []
        for i in range(1, 5):
            path = config.DIR_ASSETS + f"astroid_0{i}.png"
            try:
                img = pg.image.load(path).convert_alpha()
                self.astroid_images.append(img)
            except pg.error as e:
                print(f"Warning: Could not load {path}: {e}")

        self.bullet_color = config.YELLOW
        self.bullet_radius = 2

    def draw_ship(self, ship):
        """Draw ship rotated at current angle."""
        rotated = pg.transform.rotate(self.ship_img, -ship.angle)
        rect = rotated.get_rect(center=(ship.x, ship.y))
        self.screen.blit(rotated, rect)

    def draw_forcefield(self, forcefield):
        # Determine base color and width based on health
        health_ratio = forcefield.health / forcefield.max_health
        
        # Color transition (ex: from blue to red when damaged)
        # Interpolate between a healthy color and a danger color
        healthy_color = (0, 150, 255)  # Bright Blue
        danger_color = (255, 50, 0)    # Orange/Red
        
        r = int(healthy_color[0] + (danger_color[0] - healthy_color[0]) * (1 - health_ratio))
        g = int(healthy_color[1] + (danger_color[1] - healthy_color[1]) * (1 - health_ratio))
        b = int(healthy_color[2] + (danger_color[2] - healthy_color[2]) * (1 - health_ratio))
        color = (r, g, b)
        
        # Calculate alpha based on glow_state
        glow_range = forcefield.max_glow - forcefield.min_glow
        # Normalize glow_state (0 to 1)
        normalized_glow = (forcefield.glow_state - forcefield.min_glow) / glow_range
        # Map normalized value to the desired alpha range (ex: 50 to 200)
        alpha_min = 50
        alpha_max = 200
        alpha = int(alpha_min + (alpha_max - alpha_min) * normalized_glow)
        alpha = min(255, max(0, alpha))

        # Create a temporary Surface for drawing the transparent circle
        surface_size = (forcefield.radius * 2 + 10, forcefield.radius * 2 + 10)
        temp_surface = pg.Surface(surface_size, pg.SRCALPHA) # Use SRCALPHA flag for transparency
        temp_surface.fill((0, 0, 0, 0)) # Fill with transparent black
        
        # Draw the forcefield outline on the temporary Surface
        center = (surface_size[0] // 2, surface_size[1] // 2)
        
        # Draw the main shield
        pg.draw.circle(temp_surface, 
                       color + (alpha,),
                       center, 
                       forcefield.radius, 
                       width=3)

        # Blit the temporary surface to the main screen
        # Position the temp_surface so its center aligns with the ship's position
        rect = temp_surface.get_rect(center=(forcefield.x, forcefield.y))
        self.screen.blit(temp_surface, rect)

    def draw_bullet(self, bullet):
        pg.draw.circle(self.screen, self.bullet_color, (int(bullet.x), int(bullet.y)), self.bullet_radius)

    def draw_astroid(self, astroid):
        """Draw an astroid rotated and centered at its position."""
        img = self.astroid_images[astroid.sprite_index]

        # Scale based on astroid size
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
        colors = explosion.rings # Innermost first
        ring_width = 6 # Thickness of each ring

        # Maximum radius to hold all rings
        final_radius = ring_radius + ring_width * num_rings
        surface_size = final_radius * 2
        temp_surface = pg.Surface((surface_size, surface_size), pg.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0)) # Transparent

        center = surface_size // 2

        current_radius = ring_radius + ring_width // 2 # Start at inner radius + half width
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

    def draw_text_card(self, surface, text, x, y, size=50, text_color=config.BLACK, rect_color=config.SILVER, min_width=0, border_color=None, border_width=0):
        """Draw text with a background "card" onto the given surface."""
        font = pg.font.Font(None, size)
        text_surf = font.render(text, True, text_color)

        # Determine background rect
        text_rect = text_surf.get_rect(center=(x, y))
        required_width = max(text_rect.width, min_width)
        padding_x = 50
        padding_y = 40
        bkgd_rect = pg.Rect(0, 0, required_width + padding_x, text_rect.height + padding_y)
        bkgd_rect.center = (x, y)

        # Draw background rectangle
        pg.draw.rect(surface, rect_color, bkgd_rect, border_radius=10)

        # Draw border if specified
        if border_color and border_width > 0:
            pg.draw.rect(surface, border_color, bkgd_rect, border_radius=10, width=border_width)

        # Draw text
        surface.blit(text_surf, text_rect)

    def draw_menu(self, controller):
        banner_y = config.SCREEN_HEIGHT // 4
        banner_x = config.SCREEN_WIDTH // 2
        
        rect = self.game_banner_img.get_rect(center=(banner_x, banner_y))
        self.screen.blit(self.game_banner_img, rect)

        x = config.SCREEN_WIDTH // 2
        
        # Shift menu options down slightly to accommodate the banner
        y1 = (config.SCREEN_HEIGHT // 8) * 5 
        y2 = (config.SCREEN_HEIGHT // 8) * 6

        menu_card_width = 400
        
        rect_color = [config.SILVER] * 2
        border = [0] * 2
        text_color = [config.BLACK] * 2
        
        rect_color[controller.menu_choice_index] = config.COSMIC_PURPLE
        border[controller.menu_choice_index] = 3 
        text_color[controller.menu_choice_index] = config.SILVER

        self.draw_text_card(self.screen, "Play", x, y1, text_color=text_color[0], rect_color=rect_color[0], min_width=menu_card_width, border_color=config.VIBRANT_CYAN, border_width=border[0])
        self.draw_text_card(self.screen, "Quit", x, y2, text_color=text_color[1], rect_color=rect_color[1], min_width=menu_card_width, border_color=config.VIBRANT_CYAN, border_width=border[1])

    def draw_gameover_menu(self, controller):
        """Draw the Game Over menu on top of the gameplay screen."""
        # Semi-transparent overlay
        overlay = pg.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

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
                self.screen,
                label,
                x,
                y_start + i * spacing,
                text_color=text_color,
                rect_color=rect_color,
                min_width=400,
                border_color=border_color,
                border_width=border_width
            )

    # =============== HUD DRAWING =================

    def _create_hud_surface(self):
        """Create and return a transparent HUD surface."""
        hud_surface = pg.Surface(
            (config.SCREEN_WIDTH, config.HUD_HEIGHT),
            pg.SRCALPHA
        )
        hud_surface.fill((0, 0, 0, 0))
        return hud_surface

    def _draw_hud_background(self, surface):
        """Draws the HUD background panel."""
        surface.blit(self.hud_bkgd_img, (0, 0))

    def _draw_hud_score(self, surface, model):
        x_pos = config.SCREEN_WIDTH * 4 // 5
        y_pos = config.HUD_HEIGHT // 2
        score_text = f"Score: {model.score}"
        self.draw_text_card(
            surface,
            score_text,
            x_pos,
            y_pos,
            size=30,
            text_color=config.GREEN,
            rect_color=config.BLACK,
            min_width=120
        )

    def _draw_hud_level(self, surface, model):
        x_pos = config.SCREEN_WIDTH * 1 // 5
        y_pos = config.HUD_HEIGHT // 2
        level_text = f"Level: {model.level}"
        self.draw_text_card(
            surface,
            level_text,
            x_pos,
            y_pos,
            size=30,
            text_color=config.GREEN,
            rect_color=config.BLACK,
            min_width=100
        )

    def _draw_hud_forcefield_health(self, surface, model):
        """Draws an arc-based forcefield health indicator with pulsing when depleted."""
        component_width = 300
        component_height = config.HUD_HEIGHT * 1 // 2
        arc_thickness = 14
        gap_width = 5
        num_segments = config.FORCEFIELD_HEALTH
        num_gaps = num_segments - 1
        deg_per_segment = (180 - gap_width * num_gaps) / num_segments

        # Rectangle for the arc
        rect = (
            round(config.SCREEN_WIDTH / 2 - component_width / 2),
            round(config.HUD_HEIGHT / 4),
            round(component_width),
            round(component_height)
        )

        # Determine health info
        health_ratio = model.ship.forcefield.health / model.ship.forcefield.max_health
        active_segments = int(num_segments * health_ratio)

        # Determine segment color
        if health_ratio <= 0:
            # Pulsing red
            pulse = model.hud.glow_state  # 0–1
            # Map to alpha or brightness for pulsing effect
            alpha = int(128 + 127 * pulse)
            color = (255, 0, 0, alpha)
        else:
            if health_ratio < 0.2:
                color = config.RED
            elif health_ratio < 0.5:
                color = config.YELLOW
            else:
                color = config.GREEN

        # Draw black background rectangle behind forcefield health 
        padding = 20 
        bg_rect = pg.Rect((rect[0] - padding), (rect[1] - padding), (rect[2] + padding * 2), (rect[3] + padding * 2))
        pg.draw.rect(surface, config.BLACK, bg_rect, border_radius=10)

        self._draw_hud_text(surface, "Forcefield", (config.SCREEN_WIDTH // 2), (config.HUD_HEIGHT - 30), size=30, color=config.GREEN)

        # Draw base gray segments
        start_deg = 0.0
        for i in range(num_segments):
            end_deg = start_deg + deg_per_segment
            pg.draw.arc(
                surface,
                config.DARK_GREY,
                rect,
                math.radians(start_deg),
                math.radians(end_deg),
                arc_thickness
            )
            start_deg = end_deg + gap_width

        # Draw critical pulsing segments if forcefield depleted
        if health_ratio <= 0:
            start_deg = 0.0
            for i in range(num_segments):
                end_deg = start_deg + deg_per_segment
                pg.draw.arc(
                    surface,
                    color,
                    rect,
                    math.radians(start_deg),
                    math.radians(end_deg),
                    arc_thickness
                )
                start_deg = end_deg + gap_width

        # Draw active segments right-to-left
        end_deg = 180.0  # leftmost point
        for i in range(active_segments):
            start_deg = end_deg - deg_per_segment

            pg.draw.arc(
                surface,
                color,
                rect,
                math.radians(start_deg),
                math.radians(end_deg),
                arc_thickness
            )
            end_deg = start_deg - gap_width

    def _draw_hud_text(self, surface, text, x, y, size=30, color=config.WHITE):
        """Helper for rendering text onto HUD surfaces."""
        font = pg.font.Font(None, size)
        text_surf = font.render(text, True, color)
        rect = text_surf.get_rect(center=(x, y))
        surface.blit(text_surf, rect)

    def draw_hud(self, model):
        """Main HUD drawing function."""
        # Create HUD surface
        hud_surface = self._create_hud_surface()

        # Draw modular components
        self._draw_hud_background(hud_surface)
        self._draw_hud_score(hud_surface, model)
        self._draw_hud_level(hud_surface, model)
        self._draw_hud_forcefield_health(hud_surface, model)

        # Position HUD at the bottom of the screen
        self.screen.blit(
            hud_surface,
            (0, config.SCREEN_HEIGHT - config.HUD_HEIGHT)
        )

    # =============================================

    def render(self, controller, model):
        """Render all game objects."""
        self.screen.fill(config.BLACK)

        if controller.state in (GameState.MENU, GameState.PLAYING):
            for particle in model.particles:
                self.draw_particle(particle)

            if controller.state == GameState.MENU:
                self.draw_menu(controller)

        if controller.state in (GameState.PLAYING, GameState.PAUSED, GameState.GAMEOVER):
            for explosion in model.explosions:
                self.draw_explosion(explosion)
            
            if model.ship.alive:
                if model.ship.forcefield.health > 0:
                    self.draw_forcefield(model.ship.forcefield)
                self.draw_ship(model.ship)

            for bullet in model.ship.bullets:
                self.draw_bullet(bullet)

            for astroid in model.astroids:
                self.draw_astroid(astroid)

            if controller.state == GameState.PAUSED:
                overlay = pg.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pg.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.draw_text_card(
                    overlay,
                    "PAUSED",
                    config.SCREEN_WIDTH // 2,
                    config.SCREEN_HEIGHT // 2,
                    size=60,
                    text_color=config.GREEN,
                    rect_color=config.BLACK
                )
                self.screen.blit(overlay, (0, 0))

            if controller.state == GameState.GAMEOVER:
                self.draw_gameover_menu(controller)

            self.draw_hud(model)

        pg.display.flip()
