import pygame as pg
from model import PongModel


class PongController:
    """Controller for Pong With Guns."""
    
    def __init__(self, model: PongModel, view):
        self.model = model
        self.view = view
        self.game_mode = None
        self.score = [0, 0]
        self.MAX_SCORE = 2
        self.game_running = True

        pg.mixer.init()
        self.sound_round_start = pg.mixer.Sound('assets/round_start.mp3')

        pg.mixer.Sound.play(self.sound_round_start)

    def handle_input(self):
        """Process user input events and movement."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if not self.game_running and event.type == pg.KEYDOWN:
                if event.key == pg.K_y:
                    self.model = PongModel(self.model.width, self.model.height)
                    self.score = [0, 0]
                    self.game_running = True
                elif event.key == pg.K_n:
                    return False
            
        keys = pg.key.get_pressed()

        # --- Player 1 controls (existing) ---
        if keys[pg.K_w]:
            self.model.paddle1.set_direction(-1)  # Move up
        elif keys[pg.K_s]:
            self.model.paddle1.set_direction(1)   # Move down
        else:
            self.model.paddle1.set_direction(0)   # No movement

        if keys[pg.K_SPACE]:
            self.model.fire_bullet(1, pg.time.get_ticks() / 1000.0)

        # --- Player 2 controls (PvP mode) ---
        if self.game_mode == 'PvP':
            # Movement
            if keys[pg.K_UP]:
                self.model.paddle2.set_direction(-1)  # Move up
            elif keys[pg.K_DOWN]:
                self.model.paddle2.set_direction(1)   # Move down
            else:
                self.model.paddle2.set_direction(0)   # No movement

            # Shooting
            if keys[pg.K_RSHIFT]:
                self.model.fire_bullet(2, pg.time.get_ticks() / 1000.0)

        return True

    def update_game_state(self, dt):
        """Update model, AI shooting, and check scoring."""
        if not self.game_running:
            return

        current_time = pg.time.get_ticks() / 1000.0
        if self.game_mode == "PvAI":
            self.model.update_ai_shooting(current_time)
        self.model.update(dt, ai_enabled = (self.game_mode == "PvAI"))

        scorer = self.model.check_score()
        if scorer == 1:
            self.score[0] += 1
            pg.mixer.Sound.play(self.sound_round_start)
            self.model.reset_ball(direction_x=-1)
        elif scorer == 2:
            self.score[1] += 1
            pg.mixer.Sound.play(self.sound_round_start)
            self.model.reset_ball(direction_x=1)

        if self.score[0] >= self.MAX_SCORE or self.score[1] >= self.MAX_SCORE:
            self.game_running = False

    def select_mode(self):
        selecting = True
        mode = None
        while selecting:
            self.view.draw_start_menu()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    selecting = False
                    mode = "QUIT"
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        mode = "PvAI"
                        selecting = False
                    elif event.key == pg.K_2:
                        mode = "PvP"
                        selecting = False
                    elif event.key == pg.K_q:
                        mode = "QUIT"
                        selecting = False
        return mode