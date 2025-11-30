import pygame.math as pm
import random
import config

vec = pm.Vector2

class Obstacle:
    def __init__(self):
        self.obstacle_list = []
        self.time_since_spawn = 0
        self.spawn_interval = 1.0  # seconds
        self.distance_from_player = 500
        self.last_obstacle = None

    def update(self, dt, session):
        self.time_since_spawn += dt
        if self.time_since_spawn > self.spawn_interval:
            self.time_since_spawn = 0
            self.spawn_obstacle(session)

    def spawn_obstacle(self, session):
        if self.last_obstacle == "hole":
            obstacle_type = random.choice(["jump", "slide"])
        else:
            obstacle_type = random.choice(["jump", "slide", "hole"])

        self.last_obstacle = obstacle_type
        x_pos = session.player.pos.x + self.distance_from_player
        y_pos = 0
        obstacle_width = 50
        obstacle_height = 50

        new_obstacle = False
        if obstacle_type == "hole":
            session.ground.remove_segment_near(x_pos)
            return
        elif obstacle_type == "slide":
            new_obstacle = True
            y_pos = config.GROUND_HEIGHT - obstacle_height - 50
        elif obstacle_type == "jump":
            new_obstacle = True
            y_pos = config.GROUND_HEIGHT - obstacle_height

        if new_obstacle:
            self.obstacle_list.append({
                "type": obstacle_type, 
                "pos": vec(x_pos, y_pos), 
                "width": obstacle_width, 
                "height": obstacle_height
            })
