import pygame as pg
from model import PongModel


class PongController:
    """Controller component of Pong With Guns"""
    
    def __init__(self, model: PongModel):
        """Init controller with a game model."""
        self.model = model

    def handle_input(self):
        """Process user input events"""
        # Window events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            
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

        return True