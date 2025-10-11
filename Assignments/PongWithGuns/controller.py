import pygame as pg
from model import PongModel


class PongController:
    """Controller for Pong With Guns."""
    
    def __init__(self, model: PongModel):
        self.model = model
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

        # Player 1 movement
        p1_dir = -1 if keys[pg.K_w] or keys[pg.K_UP] else 1 if keys[pg.K_s] or keys[pg.K_DOWN] else 0
        self.model.paddle1.set_direction(p1_dir)

        # Player 2 movement
        p2_dir = -1 if keys[pg.K_UP] else 1 if keys[pg.K_DOWN] else 0
        self.model.paddle2.set_direction(p2_dir)

        # Player 1 shooting
        if self.game_running and keys[pg.K_SPACE]:
            current_time = pg.time.get_ticks() / 1000.0  # seconds
            self.model.fire_bullet(1, current_time)

        return True

    def update_game_state(self, dt):
        """Update model, AI shooting, and check scoring."""
        if not self.game_running:
            return

        current_time = pg.time.get_ticks() / 1000.0
        self.model.update_ai_shooting(current_time)
        self.model.update(dt)

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
