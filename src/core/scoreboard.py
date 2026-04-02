# src/core/scoreboard.py
import json
import os

SCORE_FILE = "data/scores.json"

class ScoreBoard:
    def __init__(self):
        self.scores = self.load_scores()

    def _ensure_data_dir(self):
        # Ensure the data directory exists
        if not os.path.exists("data"):
            os.makedirs("data")

    def load_scores(self):
        self._ensure_data_dir()
        default_struct = {"Easy": [], "Normal": [], "Hard": []}
        
        if not os.path.exists(SCORE_FILE):
            self.save_scores(default_struct)
            return default_struct
        
        try:
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)
                # Ensure backwards compat if flat array or missing difficulty keys
                if isinstance(data, list) or "Normal" not in data:
                    self.save_scores(default_struct)
                    return default_struct
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return default_struct

    def save_scores(self, scores):
        self._ensure_data_dir()
        with open(SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=4)

    def is_top_10(self, new_score, difficulty="Normal"):
        cat_scores = self.scores[difficulty]
        if len(cat_scores) < 10:
            return True
        return new_score > cat_scores[-1]["score"]

    def add_score(self, name, score, difficulty="Normal"):
        self.scores[difficulty].append({"name": name, "score": score})
        # Sort descending by score
        self.scores[difficulty].sort(key=lambda x: x["score"], reverse=True)
        # Keep only top 10
        self.scores[difficulty] = self.scores[difficulty][:10]
        self.save_scores(self.scores)

    def get_scores(self):
        return self.scores

    def reset_scores(self):
        self.scores = {"Easy": [], "Normal": [], "Hard": []}
        self.save_scores(self.scores)
