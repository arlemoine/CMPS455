import config

class Hud:
    def __init__(self):
        # Forcefield health depleted animation
        self.glow_state = 0 # Current glow progress (0-1)
        self.glow_direction = 1 # 1 = increasing, -1 = decreasing
        self.glow_speed = 0.02 # How fast it pulses per frame

    def update_critical_pulse(self, model):
        if model.ship.forcefield.health <= 0:
            self.glow_state += self.glow_direction * self.glow_speed
            if self.glow_state >= 1:
                self.glow_state = 1
                self.glow_direction = -1
            elif self.glow_state <= 0:
                self.glow_state = 0
                self.glow_direction = 1
        else:
            self.glow_state = 0
            self.glow_direction = 1
