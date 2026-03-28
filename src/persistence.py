import os
import json
from src.constants import HIGH_SCORES_FILE, DATA_PATH


def load_high_scores():
    """Reads high scores from JSON file. Returns an empty list if not found."""
    if not os.path.exists(HIGH_SCORES_FILE):
        return []
    
    try:
        with open(HIGH_SCORES_FILE, "r") as f:
            data = json.load(f)
            # Handle if the file was saved as {"high_scores": [...]} or just [...]
            if isinstance(data, dict) and "high_scores" in data:
                return data["high_scores"]
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_high_score(name: str, score: int):
    """
    Saves a new score, keeps the Top 10, and writes back to JSON.
    Returns True if the new score made it into the Top 10.
    """
    # Ensure data directory exists
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    # Load existing
    scores = load_high_scores()
    
    # Append new score and sort
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    
    # Keep only Top 10
    top_scores = scores[:10]
    
    # Write back
    try:
        with open(HIGH_SCORES_FILE, "w") as f:
            json.dump(top_scores, f, indent=4)
        
        # Check if the new entry is in the Top 10
        return any(s["name"] == name and s["score"] == score for s in top_scores)
    except IOError:
        return False
