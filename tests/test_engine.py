import pytest
import pygame
from unittest.mock import patch, MagicMock
from src.engine import GameEngine

@pytest.fixture
def mock_pygame():
    """Mocks Pygame components to prevent window initialization and video errors during tests."""
    with patch('pygame.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.image.load', return_value=pygame.Surface((64, 64))), \
         patch('pygame.time.Clock'), \
         patch('pygame.key.get_pressed', return_value=[False] * 512), \
         patch('pygame.font'):
        yield

from src.constants import FPS

def test_engine_initialization(mock_pygame):
    """Verifies that the GameEngine initializes its components correctly."""
    engine = GameEngine()
    assert engine.is_running is True
    assert FPS == 60

def test_engine_quit_event(mock_pygame):
    """Verifies that the engine stops running when a QUIT event is processed."""
    engine = GameEngine()
    
    # Create a mock QUIT event
    mock_event = MagicMock()
    mock_event.type = pygame.QUIT
    
    with patch('pygame.event.get', return_value=[mock_event]):
        engine.handle_events()
        assert engine.is_running is False
