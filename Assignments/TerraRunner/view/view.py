import pygame as pg

import config
from view.helper import load_sprite
import models.grid as grid
import models.player

class View:
    def __init__(self, session):
        self.screen = pg.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pg.display.set_caption("TerraRunner")
        self.font = pg.font.Font(None, 50)

        self.character = {
            "run1": load_sprite("assets/character/run1.png", models.player.run_width, models.player.run_height),
            "run2": load_sprite("assets/character/run2.png", models.player.run_width, models.player.run_height),
            "jump": load_sprite("assets/character/jump.png", models.player.jump_width, models.player.jump_height),
            "slide": load_sprite("assets/character/slide.png", models.player.slide_width, models.player.slide_height),
        }
        
        self.monster = {
            0: load_sprite("assets/monster/0.png", session.monster.width, session.monster.height),
            1: load_sprite("assets/monster/1.png", session.monster.width, session.monster.height),
        }

        self.ground = []
        for i in range(len(session.world.graphics["ground"])):
            sprite = load_sprite(f"assets/blocks/ground_{i}.png", config.CELL_SIZE, config.CELL_SIZE)
            self.ground.append(sprite)

        self.obstacle = []
        for i in range(len(session.world.graphics["obstacle"])):
            sprite = load_sprite(f"assets/blocks/obstacle_{i}.png", config.CELL_SIZE, config.CELL_SIZE)
            self.obstacle.append(sprite)

        self.bg_forest = load_sprite("assets/background/forest.png", config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.bg_x = 0  # current x offset
        self.bg_scroll_speed = config.BKGD_SCROLL_SPEED  # slower than foreground, e.g., 100 px/sec

    def draw_background(self, session, dt):
        """
        Draws the scrolling forest background, repeating seamlessly.
        """
        if not session.paused:
            # Move the background left
            self.bg_x -= self.bg_scroll_speed * dt

            # Wrap around when the image scrolls off-screen
            if self.bg_x <= -config.SCREEN_WIDTH:
                self.bg_x += config.SCREEN_WIDTH

        # Draw two copies to fill the screen
        self.screen.blit(self.bg_forest, (self.bg_x, 0))
        self.screen.blit(self.bg_forest, (self.bg_x + config.SCREEN_WIDTH, 0))

    def get_char_sprite(self, player):
        if player.state == models.player.PlayerState.RUN:
            return self.character["run1"] if player.run_frame == 0 else self.character["run2"]

        if player.state == models.player.PlayerState.JUMP:
            return self.character["jump"]

        if player.state == models.player.PlayerState.SLIDE:
            return self.character["slide"]

        return self.character["run1"]   # fallback

    def get_mon_sprite(self, monster):
        return self.monster[0] if monster.run_frame == 0 else self.monster[1]

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
            if block.block_type == "ground":
                # Use sprite based on block_type_index
                sprite = self.ground[block.block_type_index]
                self.screen.blit(sprite, (block.pos.x, block.pos.y))
            elif block.block_type == "obstacle":
                sprite = self.obstacle[block.block_type_index]
                self.screen.blit(sprite, (block.pos.x, block.pos.y))
            else:
                pg.draw.rect(self.screen, config.BLACK, (block.pos.x, block.pos.y, block.width, block.height))

    def draw_player(self, session):
        player = session.player
        sprite = self.get_char_sprite(player)
        self.screen.blit(sprite, (player.pos.x, player.pos.y))

    def draw_monster(self, session):
        monster = session.monster
        sprite = self.get_mon_sprite(monster)
        if monster.active:
            self.screen.blit(sprite, (monster.pos.x, monster.pos.y))

    def spawn_message(self, monster):
        """
        Render the monster's spawn message on the screen with fading effect.
        """
        msg = monster.spawn_msg
        if not msg["active"]:
            return

        # Create text surface with red color
        font = pg.font.Font(None, 50)
        text_surf = font.render(msg["text"], True, (255, 0, 0))

        # Apply alpha (transparency)
        text_surf.set_alpha(msg["alpha"])

        # Center message horizontally, slightly above middle of screen
        rect = text_surf.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 3))
        self.screen.blit(text_surf, rect)

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

    def draw_game_over_screen(self, controller, score):
        """
        Draws the Game Over screen as a transparent overlay over the last frame.
        """
        # Semi-transparent overlay
        overlay = pg.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(180)  # adjust transparency
        overlay.fill(config.DARK_GREY)
        self.screen.blit(overlay, (0, 0))

        # --- Game Over title ---
        font = pg.font.Font(None, 120)
        title_surf = font.render("GAME OVER", True, config.RED)
        title_rect = title_surf.get_rect(center=(config.SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)

        # --- Final score ---
        score_font = pg.font.Font(None, 60)
        score_surf = score_font.render(f"Score: {int(score)}", True, config.WHITE)
        score_rect = score_surf.get_rect(center=(config.SCREEN_WIDTH // 2, 250))
        self.screen.blit(score_surf, score_rect)

        # --- Buttons ---
        game_over_options = ["PLAY", "MAIN MENU", "QUIT"]
        button_spacing = 120
        start_y = 400
        for i, option in enumerate(game_over_options):
            highlighted = (option == controller.game_over_hover)
            center_pos = (config.SCREEN_WIDTH // 2, start_y + i * button_spacing)
            self.draw_button(option, center_pos, highlighted=highlighted)

    def render_playing(self, controller, session, dt):
        self.draw_background(session, dt)
        self.draw_world_blocks(session)
        self.draw_player(session)
        self.draw_monster(session)
        self.draw_score(session)

        # Draw monster spawn message
        self.spawn_message(session.monster)

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

        if controller.mode == "game_over":
            self.draw_game_over_screen(controller, session.score_tracker.score)

    def render(self, controller, session, dt):
        self.screen.fill(config.WHITE)
        self.draw_grid()

        if controller.mode == "menu":
            self.render_menu(controller)
        elif controller.mode == "playing" or controller.mode == "game_over":
            self.render_playing(controller, session, dt)

        pg.display.flip()
