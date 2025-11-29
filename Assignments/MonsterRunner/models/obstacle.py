import pygame.math.Vector2 as vec
import random

class Obstacle:
    def __init__(self):
        self.list = [] 
        self.time_since_last_spawn = 0
        self.spawn_interval = 0.8 # Seconds
        self.pos = vec(0, 0) # Holds the position a set distance ahead of the player for generating obstacles

    def update(self, dt, session):
        self.pos = session.player.pos + vec(1000, 0)
        self.time_since_last_spawn += dt
        if self.time_since_last_spawn > self.spawn_interval:
            self.time_since_last_spawn = 0
            self.spawn_obstacle(session)

    def spawn_obstacle(self, session):
        obstacle_type = random.choice(['jump', 'slide', 'hole'])
        match obstacle_type:
            case 'jump':
                self.create_jump_obstacle()
            case 'slide':
                self.create_slide_obstacle()
            case 'hole':
                self.create_hole_obstacle(session)

    def create_jump_obstacle(self):
        self.list.append({
            "type": "jump",
            "pos": self.pos,
            "width": 50,
            "height": 50
        })

    def create_slide_obstacle(self):
        self.list.append({
            "type": "slide",
            "pos": self.pos + vec(0, 50),
            "width": 50,
            "height": 50
        })

    def create_hole_obstacle(self, session):
        self.list.append({
            "type": "hole",
            "pos": vec(self.pos.x, session.ground.height),
            "width": 100,
            "height": session.ground.height
        })
