# src/core/scoreboard.py
import json
import os

SCORE_FILE = "data/scores.json"

class ScoreBoard:
    def __init__(self) -> None:
        self.scores: dict[str, list[dict]] = self.load_scores()

    def _ensure_data_dir(self) -> None:
        if not os.path.exists("data"):
            os.makedirs("data")

    def load_scores(self) -> dict[str, list[dict]]:
        self._ensure_data_dir()
        default: dict[str, list[dict]] = {"Easy": [], "Normal": [], "Hard": []}

        if not os.path.exists(SCORE_FILE):
            self.save_scores(default)
            return default

        try:
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list) or "Normal" not in data:
                    self.save_scores(default)
                    return default
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return default

    def save_scores(self, scores: dict[str, list[dict]]) -> None:
        self._ensure_data_dir()
        with open(SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=4)

    def is_top_10(self, new_score: int, difficulty: str = "Normal") -> bool:
        cat = self.scores[difficulty]
        if len(cat) < 10:
            return True
        return new_score > cat[-1]["score"]

    def add_score(self, name: str, score: int, difficulty: str = "Normal") -> None:
        self.scores[difficulty].append({"name": name, "score": score})
        self.scores[difficulty].sort(key=lambda x: x["score"], reverse=True)
        self.scores[difficulty] = self.scores[difficulty][:10]
        self.save_scores(self.scores)

    def get_scores(self) -> dict[str, list[dict]]:
        return self.scores

    def reset_scores(self) -> None:
        self.scores = {"Easy": [], "Normal": [], "Hard": []}
        self.save_scores(self.scores)
