import config # Assuming this holds constants you might use

class Forcefield:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 34
        self.max_health = config.FORCEFIELD_HEALTH
        self.health = self.max_health
        
        # Base Glow Effect Variables
        self.min_glow = 5
        self.max_glow = 10
        self.glow_state = self.max_glow
        self.glow_direction = -1 # -1 for decreasing, 1 for increasing
        self.base_glow_speed = 0.05 # Base speed, modified by health
        
        # Damage Flash Variables
        self.flash_timer = 0
        self.flash_duration = 5 # How many frames the flash lasts (adjust as needed)
        self.flash_intensity = 15 # A very high glow value for the flash
        
    def recenter(self, x, y):
        self.x = x
        self.y = y

    def damage(self):
        if self.health > 0:
            self.health -= 1
            
            # Trigger the damage flash
            self.flash_timer = self.flash_duration
            
            return True
        return False

    def update(self):
        # The glow speed increases as health drops (pulse faster when damaged).
        health_ratio = self.health / self.max_health
        speed_multiplier = 1 + (1 - health_ratio) 
        current_glow_speed = self.base_glow_speed * speed_multiplier
        
        if self.flash_timer <= 0:
            # Only pulse if not flashing
            if self.glow_state >= self.max_glow:
                self.glow_direction = -1
            elif self.glow_state <= self.min_glow:
                self.glow_direction = 1

            self.glow_state += self.glow_direction * current_glow_speed 
            self.glow_state = max(self.min_glow, min(self.max_glow, self.glow_state))
            
        if self.flash_timer > 0:
            # While flashing, force the glow state to a high intensity and count down.
            self.glow_state = self.flash_intensity 
            self.flash_timer -= 1
            
        # When the flash ends, immediately reset to the max/mid-point of the normal pulse
        if self.flash_timer == 0 and self.glow_state == self.flash_intensity:
            self.glow_state = self.max_glow
            self.glow_direction = -1
