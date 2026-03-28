class GameSession:
    """
    Shared state object to carry data across different game scenes (states).
    Tracks current score, high scores, and session-specific results.
    """
    def __init__(self):
        self.current_score: int = 0
        self.last_score: int = 0
        self.is_new_high_score: bool = False
        self.high_scores: list = [] # Top 10 rankings

    def reset_session(self):
        """Resets the score for a new game run."""
        self.last_score = self.current_score
        self.current_score = 0
        self.is_new_high_score = False
