import pygame.math.Vector2 as vec

import config 

def check_collision(object1, object2):
    # Ground collision
    if object1.pos >= config.SCREEN_HEIGHT - object1.height - object2.height:
        object1.pos.y = config.SCREEN_HEIGHT - object1.height - object2.height
        object1.vel.y = 0
        object1.on_ground = True