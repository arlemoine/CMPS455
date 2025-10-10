import pygame as pg
from model import PongModel


class PongController:
    """Controller component of Pong With Guns"""
    
    def __init__(self, model: PongModel):
        """Init controller with a game model."""
        self.model = model
        self.score = [0, 0]
        self.MAX_SCORE = 5
        self.game_running = True

    def handle_input(self):
        """Process user input events"""
        # Window events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if not self.game_running:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_y:
                        # Create new model, reset persistent score, and resume game
                        self.model = PongModel(self.model.width, self.model.height)
                        self.score = [0, 0]
                        self.game_running = True
                    elif event.key == pg.K_n:
                        return False # Quit the application
            
        # Continuous key presses (movement)
        keys = pg.key.get_pressed()

        p1_direction = 0
        if keys[pg.K_w]:
            p1_direction = -1 # Up
        if keys[pg.K_s]: 
            p1_direction = 1 # Down

        self.model.paddle1.set_direction(p1_direction)

        p2_direction = 0
        if keys[pg.K_UP]:
            p2_direction = -1 # Up
        if keys[pg.K_DOWN]:
            p2_direction = 1  # Down
            
        self.model.paddle2.set_direction(p2_direction)

        if self.game_running:
            current_time = pg.time.get_ticks() / 1000.0 # Convert ms to seconds
            
            if keys[pg.K_SPACE]:
                # Fire bullet for Player 1
                self.model.fire_bullet(1, current_time)

        return True

    def update_game_state(self, dt):
        """Updates the model and checks for score/win conditions."""
        if not self.game_running:
            return 
            
        current_time = pg.time.get_ticks() / 1000.0 
        self.model.update_ai_shooting(current_time) 

        self.model.update(dt) 
            
        scorer = self.model.check_score()
        
        if scorer == 1:
            self.score[0] += 1
            # ⭐ NEW: Reset the ball after Player 1 scores, launching towards P2 (-1) ⭐
            self.model.reset_ball(direction_x=-1) 
        elif scorer == 2:
            self.score[1] += 1
            # ⭐ NEW: Reset the ball after Player 2 scores, launching towards P1 (1) ⭐
            self.model.reset_ball(direction_x=1) 
            
        if self.score[0] >= self.MAX_SCORE or self.score[1] >= self.MAX_SCORE:
            self.game_running = False