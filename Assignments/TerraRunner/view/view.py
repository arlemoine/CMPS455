import pygame as pg

import config
import models.grid as grid

class View:
    def __init__(self):
        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption("MonsterRunner")
        self.font = pg.font.Font(None, 50)

    def draw_grid(self):
        """
        Draws the entire grid on the given Pygame surface.
        """
        for i in range(grid.num_cells_x):
            for j in range(grid.num_cells_y):
                x0, y0, x1, y1 = grid.get_cell_bounds(i, j)
                rect = pg.Rect(x0, y0, config.CELL_SIZE, config.CELL_SIZE)
                pg.draw.rect(self.screen, config.SILVER, rect, width=1)

    def draw_world_blocks(self, session):
        world = session.world

        for block in world.blocks:

            if block.block_type == "ground": block_color = config.GREEN
            elif block.block_type == "obstacle": block_color = config.RED
            else: block_color = config.BLACK

            pg.draw.rect(self.screen, block_color, (block.pos.x, block.pos.y, block.width, block.height))

    def draw_player(self, session):
        player = session.player
        pg.draw.rect(self.screen, config.BLUE, (player.pos.x, player.pos.y, player.width, player.height))

    def draw_monster(self, session):
        monster = session.monster
        if monster.active:
            pg.draw.rect(self.screen, config.ORANGE, (monster.pos.x, monster.pos.y, monster.width, monster.height))

    def draw_score(self, session):
        """
        Draws the current score and high score on screen.
        """
        score_text = f"Score: {int(session.score_tracker.score)}"
        high_text = f"High: {int(session.score_tracker.high_score)}"

        # Render text surfaces
        score_surf = self.font.render(score_text, True, config.BLACK)
        high_surf = self.font.render(high_text, True, config.BLACK)

        # Position on screen (top-left corner)
        self.screen.blit(score_surf, (20, 20))
        self.screen.blit(high_surf, (20, 70))

    def draw_button(self, text, center_pos, width=300, height=80, highlighted=False):
        """
        Draws a single squircle-style button with text.
        
        :param text: str, text to render on button
        :param center_pos: tuple, (x, y) center of button
        :param width: int, button width
        :param height: int, button height
        :param highlighted: bool, if True, use highlight color
        """
        # Colors
        base_color = config.DARK_GREY
        highlight_color = config.GREEN
        text_color = config.WHITE if not highlighted else config.BLACK

        color = highlight_color if highlighted else base_color

        # Rect centered at center_pos
        rect = pg.Rect(0, 0, width, height)
        rect.center = center_pos

        # Draw squircle (rounded rectangle)
        pg.draw.rect(self.screen, color, rect, border_radius=24)

        # Draw text
        font_surf = self.font.render(text, True, text_color)
        font_rect = font_surf.get_rect(center=rect.center)
        self.screen.blit(font_surf, font_rect)

    def draw_main_menu(self, controller):
        """
        Draw the main menu screen.

        :param controller: Controller instance to access hover state and options
        """
        # # Clear screen
        # self.screen.fill(config.BKGD_COLOR)

        # --- Draw Game Title as Image ---
        title_img = pg.image.load(str(config.DIR_ASSETS / "main" / "title_graphic.png")).convert_alpha()
        title_rect = title_img.get_rect(center=(config.SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_img, title_rect)

        # --- Draw Menu Buttons ---
        button_spacing = 120  # vertical spacing between buttons
        start_y = config.SCREEN_HEIGHT / 2         # starting y position for first button

        for i, option in enumerate(controller.main_menu_options):
            highlighted = (option == controller.main_menu_hover)
            center_pos = (config.SCREEN_WIDTH // 2, start_y + i * button_spacing)
            self.draw_button(option, center_pos, highlighted=highlighted)

        # Flip the display
        pg.display.flip()

    def render_menu(self, controller):
        self.draw_main_menu(controller)

    def render_playing(self, session):
        self.draw_world_blocks(session)
        self.draw_player(session)
        self.draw_monster(session)
        self.draw_score(session)

        if session.paused:
            # Overlay semi-transparent layer to simulate blur
            overlay = pg.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            overlay.set_alpha(120)  # transparency
            overlay.fill(config.DARK_GREY)
            self.screen.blit(overlay, (0, 0))

            # Draw PAUSED text
            pause_font = pg.font.Font(None, 120)
            text_surf = pause_font.render("PAUSED", True, config.GREEN)
            text_rect = text_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
            self.screen.blit(text_surf, text_rect)

    def render(self, controller, session):
        self.screen.fill(config.WHITE)
        self.draw_grid()

        if controller.mode == "menu":
            self.render_menu(controller)
        elif controller.mode == "playing":
            self.render_playing(session)

        pg.display.flip()
