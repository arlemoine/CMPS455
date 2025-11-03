import config

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 17
        self.num_rings = config.NUM_RINGS
        self.colors = [
            (255, 255, 255), (255, 250, 240), (255, 245, 220), (255, 235, 200),
            (255, 225, 180), (255, 210, 150), (255, 195, 120), (255, 180, 90),
            (255, 165, 60), (240, 145, 50), (225, 130, 45), (210, 115, 40),
            (195, 100, 35), (180, 85, 30), (165, 70, 25), (150, 55, 20),
            (135, 45, 15), (120, 35, 10), (100, 25, 10), (80, 20, 10),
            (60, 15, 10), (40, 10, 5), (20, 5, 2), (0, 0, 0)
        ]
        self.duration = config.EXPLOSION_DURATION  # seconds for full animation
        self.elapsed = 0.0
        self.rings = [self.colors[0]] * self.num_rings  # start all bright
        self.alive = True

    def update(self, dt):
        if not self.alive:
            return

        self.elapsed += dt
        total_colors = len(self.colors)

        # Time each ring should start its propagation
        ring_delay = self.duration / self.num_rings

        for i in range(self.num_rings):
            # How long this ring has been propagating
            ring_elapsed = self.elapsed - i * ring_delay
            ring_elapsed = max(0.0, ring_elapsed)

            # Map elapsed time to color index
            color_progress = min(1.0, ring_elapsed / self.duration)
            color_index = int(color_progress * (total_colors - 1))
            color_index = min(total_colors - 1, color_index)
            self.rings[i] = self.colors[color_index]

        # Explosion ends when outermost ring has fully transitioned
        if self.elapsed >= self.duration + ring_delay * (self.num_rings - 1):
            self.alive = False

