from pygame.math import Vector2 as vec

import config

class Ground:
    def __init__(self):
        self.segment_list = []
        self.next_x = 0
        self.spawn_distance = 500
        self.segment_width = 100
        self.segment_height = 100
        self.segment_despawn_distance = 500

        for i in range(10):
            self.spawn_segment()

    def spawn_segment(self): 
        segment = {
            "pos": vec(self.next_x, config.GROUND_HEIGHT),
            "width": self.segment_width,
            "height": self.segment_height
        }
        self.next_x += self.segment_width
        self.segment_list.append(segment)

    def remove_segment_near(self, x_pos):
        for segment in self.segment_list:
            if segment["pos"].x + segment["width"] > x_pos:
                self.segment_list.remove(segment)
                break

    def update(self, dt, player):
        if self.next_x < (player.pos.x + self.spawn_distance):
            self.spawn_segment()

        new_segment_list = []

        for segment in self.segment_list:
            segment_right_edge = segment["pos"].x + self.segment_width
            despawn_x = player.pos.x - self.segment_despawn_distance
            if segment_right_edge >= despawn_x:
                new_segment_list.append(segment)

        self.segment_list = new_segment_list