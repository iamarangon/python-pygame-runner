import pytest
import pygame
from unittest.mock import patch
from src.state_manager import StateManager
from src.state_enums import GameState

@pytest.fixture(autouse=True)
def mock_pygame():
    """Mocks Pygame components for all StateManager tests."""
    with patch('pygame.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.image.load', return_value=pygame.Surface((64, 64))), \
         patch('pygame.font'):
        yield

def test_state_manager_initial_state():
    """Verifies that the StateManager starts in the MENU state by default."""
    manager = StateManager()
    assert manager.current_state == GameState.MENU

def test_state_manager_initial_custom_state():
    """Verifies that the StateManager can start in a custom state."""
    manager = StateManager(initial_state=GameState.PLAYING)
    assert manager.current_state == GameState.PLAYING

def test_state_manager_change_state():
    """Verifies that state transitions are handled correctly."""
    manager = StateManager()
    manager.change_state(GameState.PLAYING)
    assert manager.current_state == GameState.PLAYING
    
    manager.change_state(GameState.GAME_OVER)
    assert manager.current_state == GameState.GAME_OVER

def test_state_manager_read_only_property():
    """Verifies that the current_state property is read-only (protected via property decorator)."""
    manager = StateManager()
    with pytest.raises(AttributeError):
        # This should fail as there is no setter for current_state
        manager.current_state = GameState.PLAYING
