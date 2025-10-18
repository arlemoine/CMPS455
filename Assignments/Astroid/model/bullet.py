import math
import config

class Bullet:
    def __init__(self, x, y, angle):
        self.angle_rad = math.radians(angle - 90)

        offset_x = config.BULLET_OFFSET * math.cos(self.angle_rad)
        offset_y = config.BULLET_OFFSET * math.sin(self.angle_rad)

        self.x_start = x + offset_x
        self.y_start = y + offset_y
        self.x = self.x_start
        self.y = self.y_start
        self.vx = config.BULLET_SPEED * math.cos(self.angle_rad)
        self.vy = config.BULLET_SPEED * math.sin(self.angle_rad)
        self.distance = 0
        self.expired = False

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.update_distance()
        if self.distance > config.BULLET_MAX_DISTANCE:
            self.expired = True

    def update_distance(self):
        x1 = abs(self.x_start - self.x)
        x2 = abs(self.y_start - self.y)
        self.distance = math.sqrt((x1 ** 2) + (x2 ** 2))
