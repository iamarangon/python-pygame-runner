import pytest
import os
import json
from src.core.scoreboard import ScoreBoard

@pytest.fixture
def mock_score_file(tmp_path, monkeypatch):
    """Fixture that intercepts reading/writing scores to point to a temporary test directory."""
    test_file = tmp_path / "scores.json"
    
    # We patch SCORE_FILE inside the module to point to our test temporary path
    import src.core.scoreboard as sb_module
    monkeypatch.setattr(sb_module, "SCORE_FILE", str(test_file))
    
    # Pre-populate with known default data before each test
    default_data = {
        "Easy": [{"name": "TST", "score": 50 - i} for i in range(10)],
        "Normal": [{"name": "TST", "score": 50 - i} for i in range(10)],
        "Hard": [{"name": "TST", "score": 50 - i} for i in range(10)]
    }
    os.makedirs(tmp_path, exist_ok=True)
    with open(test_file, "w") as f:
        json.dump(default_data, f)
        
    return str(test_file)

def test_scoreboard_load(mock_score_file):
    board = ScoreBoard()
    scores = board.get_scores()
    
    assert len(scores["Normal"]) == 10
    assert scores["Normal"][0]["name"] == "TST"
    assert scores["Normal"][0]["score"] == 50

def test_scoreboard_is_top_10(mock_score_file):
    board = ScoreBoard()
    # The lowest score in our mock data is 50-9 = 41
    # So essentially > 41 is True
    assert board.is_top_10(50, "Normal") is True
    assert board.is_top_10(45, "Normal") is True
    assert board.is_top_10(5, "Normal") is False

def test_scoreboard_add_score(mock_score_file):
    board = ScoreBoard()
    board.add_score("NEW", 100, "Normal")
    
    scores = board.get_scores()
    assert len(scores["Normal"]) == 10 # Should truncate back to 10
    assert scores["Normal"][0]["name"] == "NEW"
    assert scores["Normal"][0]["score"] == 100
    
    # The lowest score is now 50 - 8 = 42
    assert scores["Normal"][-1]["score"] == 42
    
def test_scoreboard_no_file(mock_score_file, tmp_path, monkeypatch):
    # Test behavior when file is completely absent
    empty_file = tmp_path / "nothere.json"
    import src.core.scoreboard as sb_module
    monkeypatch.setattr(sb_module, "SCORE_FILE", str(empty_file))
    
    board = ScoreBoard()
    scores = board.get_scores()
    assert len(scores["Normal"]) == 0

def test_scoreboard_reset(mock_score_file):
    board = ScoreBoard()
    board.add_score("XXX", 9999, "Normal")
    assert board.get_scores()["Normal"][0]["name"] == "XXX"
    
    board.reset_scores()
    scores = board.get_scores()
    assert len(scores["Normal"]) == 0
