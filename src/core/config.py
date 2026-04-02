# src/core/config.py
import json
import os

CONFIG_FILE = "data/config.json"

class Config:
    def __init__(self):
        # Default Settings
        self.volume = 2 # Maps to [0.0, 0.25, 0.5, 0.75, 1.0] -> 2 is 0.5
        self.difficulty = "Normal" # "Easy", "Normal", "Hard"
        self.diff_multiplier = {"Easy": 0.5, "Normal": 1.0, "Hard": 1.5}
        
        self.load()

    def _ensure_dir(self):
        if not os.path.exists("data"):
            os.makedirs("data")

    def load(self):
        self._ensure_dir()
        if not os.path.exists(CONFIG_FILE):
            self.save()
            return
            
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.volume = min(max(data.get("volume", 2), 0), 4) # bound 0 to 4
                self.difficulty = data.get("difficulty", "Normal")
                if self.difficulty not in self.diff_multiplier:
                    self.difficulty = "Normal"
        except (json.JSONDecodeError, FileNotFoundError):
            self.save()

    def save(self):
        self._ensure_dir()
        data = {
            "volume": self.volume,
            "difficulty": self.difficulty
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
            
    def get_music_volume(self):
        return self.volume * 0.25
        
    def get_difficulty_factor(self):
        return self.diff_multiplier[self.difficulty]
