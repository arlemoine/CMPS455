import config
import random

class Ground:
    def __init__(self):
        self.segments = []
        self.starting_spot = 0

        for i in range(3):
            self.get_random_segment()

    def add_segment(self, slope_type):
        self.segments.append(slope_type)

    def get_random_segment(self):
        choices = [FlatSegment, InclineSegment, DeclineSegment]
        choice = random.choice(choices)
        print(f"choice: {choice}")
        self.segments.append(choice())

class FlatSegment:
    def __init__(self, height_factor=1, length=100):
        self.length = length
        self.lheight = config.HEIGHT_CONSTANT * height_factor
        self.rheight = config.HEIGHT_CONSTANT * height_factor

class InclineSegment:
    def __init__(self, height_factor=1, length=100):
        self.length = length
        self.lheight = config.HEIGHT_CONSTANT * height_factor
        self.rheight = config.HEIGHT_CONSTANT * height_factor + config.HEIGHT_CONSTANT

class DeclineSegment:
    def __init__(self, height_factor=1, length=100):
        self.length = length
        self.lheight = config.HEIGHT_CONSTANT * height_factor
        self.rheight = config.HEIGHT_CONSTANT * height_factor - config.HEIGHT_CONSTANT

if __name__ == "__main__":
    ground = Ground()
    ground.get_random_segment()
    print(type(ground.segments[0]))

