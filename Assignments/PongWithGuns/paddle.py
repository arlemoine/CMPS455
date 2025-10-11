import pygame as pg

class Paddle:
    """Model for Pong paddle."""

    def __init__(self, x: int, y: int, bound_top: int, bound_bottom: int):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 80
        self.original_height = self.height

        self.MIN_Y = bound_top + (self.height // 2)
        self.MAX_Y = bound_bottom - (self.height // 2)
        
        self.hitbox_buffer = 10
        self.hitbox_x1 = self.x - self.hitbox_buffer
        self.hitbox_y1 = self.y - self.hitbox_buffer
        self.hitbox_x2 = self.hitbox_x1 + self.width + 2 * self.hitbox_buffer
        self.hitbox_y2 = self.hitbox_y1 + self.height + 2 * self.hitbox_buffer

        self.base_speed = 240  # pixels per second
        self.speed = self.base_speed
        self.direction = 0

        # Growth/shrink properties
        self.MIN_HEIGHT = 14
        self.SHRINK_AMOUNT = 8
        self.GROWTH_RATE = 2.0  # pixels per second
        self.last_hit_time = -10  # Regrowth can start immediately if needed

    def set_direction(self, direction: int = 0):
        self.direction = direction

    def move(self, dt):
        """Move paddle vertically based on direction and speed."""
        self.y += self.speed * self.direction * dt
        self.y = max(self.MIN_Y, min(self.y, self.MAX_Y))
        self.update_hitbox()

    def update_hitbox(self):
        """Recalculate paddle hitbox from center coordinates."""
        half_height = self.height // 2
        self.hitbox_x1 = self.x - self.hitbox_buffer
        self.hitbox_x2 = self.hitbox_x1 + self.width + 2 * self.hitbox_buffer
        self.hitbox_y1 = self.y - half_height - self.hitbox_buffer
        self.hitbox_y2 = self.y + half_height + self.hitbox_buffer

    def update_size(self, dt):
        """Regrow paddle height over time until original size."""
        current_time = pg.time.get_ticks() / 1000.0
        if self.height < self.original_height and (current_time - self.last_hit_time) > 10:
            self.height += self.GROWTH_RATE * dt
            self.speed = self.base_speed * (self.height / self.original_height)
            if self.height > self.original_height:
                self.height = self.original_height
                self.speed = self.base_speed

    def shrink_on_hit(self):
        """Shrink paddle height when hit and adjust speed and hitbox."""
        self.height -= self.SHRINK_AMOUNT
        if self.height < self.MIN_HEIGHT:
            self.height = self.MIN_HEIGHT
        self.speed = self.base_speed * (self.height / self.original_height)
        self.update_hitbox()
