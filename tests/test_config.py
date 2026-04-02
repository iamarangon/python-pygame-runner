import pytest
import os
import json
from src.core.config import Config

def test_config_save_load(tmp_path, monkeypatch):
    test_file = tmp_path / "config.json"
    import src.core.config as cfg_module
    monkeypatch.setattr(cfg_module, "CONFIG_FILE", str(test_file))
    
    config = Config()
    assert config.volume == 2
    assert config.difficulty == "Normal"
    
    config.volume = 4
    config.difficulty = "Hard"
    config.save()
    
    config2 = Config()
    assert config2.volume == 4
    assert config2.difficulty == "Hard"

def test_config_getters(tmp_path, monkeypatch):
    test_file = tmp_path / "config.json"
    import src.core.config as cfg_module
    monkeypatch.setattr(cfg_module, "CONFIG_FILE", str(test_file))
    
    config = Config()
    config.volume = 2
    config.difficulty = "Easy"
    assert config.get_music_volume() == 0.5
    assert config.get_difficulty_factor() == 0.5
    
    config.difficulty = "Hard"
    assert config.get_difficulty_factor() == 1.5

def test_config_corrupted(tmp_path, monkeypatch):
    test_file = tmp_path / "config.json"
    import src.core.config as cfg_module
    monkeypatch.setattr(cfg_module, "CONFIG_FILE", str(test_file))
    
    with open(test_file, 'w') as f:
        f.write("{garbage]")
        
    config = Config()
    assert config.volume == 2
    assert config.difficulty == "Normal"
