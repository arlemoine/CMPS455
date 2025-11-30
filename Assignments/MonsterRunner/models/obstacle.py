import pygame.math as pm
import random
import config

vec = pm.Vector2

class Obstacle:
    def __init__(self, width, pos):
        self.height = 50
        self.width = width
        self.pos = pos
        self.type = None