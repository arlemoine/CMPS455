from pygame.math import Vector2 as vec

import config

segment_width, segment_height = 100, 50

class GroundSegment:
    def __init__(self, pos):
        self.pos = pos
        self.width, height = segment_width, segment_height

class Ground:
    def __init__(self):
        self.segments = []
        self.next_pos = vec(0, config.GROUND_HEIGHT)

        for i in range(10):
            self.add_segment()

    def update(self, dt):
        for segment in self.segments:
            segment.pos += vec(-50, 0) * dt

        if self.segments[0].pos.x < config.HARD_BOUND_LEFT:
            del self.segments[0]
            self.add_segment()

    def add_segment(self):
        self.segments.append(GroundSegment(self.next_pos))
        self.next_pos += segment_width

    def get_tail_x(self):
        segment_list_length = len(self.segments)
        tail_segment = self.segments[segment_list_length - 1]
        tail_x = tail_segment.pos.x + tail_segment.width
        return tail_x