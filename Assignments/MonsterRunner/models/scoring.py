import json
import os

class ScoreTracker:
    def __init__(self, save_path="highscore.json"):
        self.score = 0
        self.distance = 0.0

        self.save_path = save_path
        self.high_score = 0

        self._load_high_score()

    def update(self, dt, world_speed):
        distance_gained = world_speed.x * dt
        self.distance += distance_gained
        self.score += distance_gained

    def reset(self):
        self.score = 0
        self.distance = 0.0

    # --------------------------
    # High Score Logic
    # --------------------------
    def _load_high_score(self):
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
            except:
                self.high_score = 0

    def _save_high_score(self):
        try:
            with open(self.save_path, "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except:
            pass

    def finalize_run(self):
        """
        Call this when the run ends (player death / caught / restart).
        Saves high score if needed.
        """
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()
