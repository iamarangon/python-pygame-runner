# src/core/config.py
import json
import os

CONFIG_FILE = "data/config.json"
DIFFICULTY_LEVELS: list[str] = ["Easy", "Normal", "Hard"]

class Config:
    def __init__(self) -> None:
        self.volume: int = 2
        self.difficulty: str = "Normal"
        self._diff_multiplier: dict[str, float] = {
            "Easy": 0.5,
            "Normal": 1.0,
            "Hard": 1.5,
        }
        self.load()

    def _ensure_dir(self) -> None:
        if not os.path.exists("data"):
            os.makedirs("data")

    def load(self) -> None:
        self._ensure_dir()
        if not os.path.exists(CONFIG_FILE):
            self.save()
            return
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.volume = min(max(data.get("volume", 2), 0), 4)
                self.difficulty = data.get("difficulty", "Normal")
                if self.difficulty not in self._diff_multiplier:
                    self.difficulty = "Normal"
        except (json.JSONDecodeError, FileNotFoundError):
            self.save()

    def save(self) -> None:
        self._ensure_dir()
        with open(CONFIG_FILE, "w") as f:
            json.dump({"volume": self.volume, "difficulty": self.difficulty}, f, indent=4)

    def get_music_volume(self) -> float:
        return self.volume * 0.25

    def get_difficulty_factor(self) -> float:
        return self._diff_multiplier[self.difficulty]
