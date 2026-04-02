import pytest
import json
import os
from src.core.scoreboard import ScoreBoard


@pytest.fixture
def clean_scoreboard(tmp_path, monkeypatch):
    test_file = tmp_path / "scores.json"
    import src.core.scoreboard as sb_module
    monkeypatch.setattr(sb_module, "SCORE_FILE", str(test_file))
    return str(test_file)


class TestScoreboardEdgeCases:
    def test_load_flat_list_resets_to_dict(self, clean_scoreboard):
        """If scores.json has an old flat list, it migrates to dict structure."""
        with open(clean_scoreboard, "w") as f:
            json.dump([{"name": "AAA", "score": 100}], f)

        sb = ScoreBoard()
        scores = sb.get_scores()
        assert isinstance(scores, dict)
        assert "Normal" in scores
        assert scores["Normal"] == []

    def test_load_missing_normal_key_resets(self, clean_scoreboard):
        """If 'Normal' key is missing, resets to default structure."""
        with open(clean_scoreboard, "w") as f:
            json.dump({"Easy": []}, f)  # Missing "Normal"

        sb = ScoreBoard()
        scores = sb.get_scores()
        assert "Normal" in scores
        assert "Hard" in scores

    def test_is_top_10_when_less_than_10_entries(self, clean_scoreboard):
        """Always top 10 when fewer than 10 scores exist."""
        sb = ScoreBoard()
        assert sb.is_top_10(1, "Hard") is True

    def test_is_top_10_when_full_and_low_score(self, clean_scoreboard):
        """Returns False when list is full and score is too low."""
        sb = ScoreBoard()
        for i in range(10):
            sb.add_score("ZZZ", 1000 - i, "Easy")
        assert sb.is_top_10(1, "Easy") is False

    def test_add_score_all_difficulties(self, clean_scoreboard):
        """Scores go into the correct bucket for each difficulty."""
        sb = ScoreBoard()
        sb.add_score("EZY", 100, "Easy")
        sb.add_score("NRM", 200, "Normal")
        sb.add_score("HRD", 300, "Hard")

        scores = sb.get_scores()
        assert scores["Easy"][0]["name"] == "EZY"
        assert scores["Normal"][0]["name"] == "NRM"
        assert scores["Hard"][0]["name"] == "HRD"
