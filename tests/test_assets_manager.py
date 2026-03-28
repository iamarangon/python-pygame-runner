import pytest
import os
from unittest.mock import patch, MagicMock
from src.assets_manager import AssetManager


@pytest.fixture
def mock_pygame_init():
    """Mocks Pygame and OS components to prevent actual file loading."""
    with patch('pygame.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.image.load') as mock_load, \
         patch('pygame.font.Font') as mock_font, \
         patch('pygame.font.SysFont') as mock_sysfont, \
         patch('os.path.exists', return_value=True): # Mock all files as existing
        # Mock load returning unique objects for each call
        mock_load.side_effect = lambda *args, **kwargs: MagicMock()
        mock_font.side_effect = lambda *args, **kwargs: MagicMock()
        mock_sysfont.side_effect = lambda *args, **kwargs: MagicMock()
        yield mock_load, mock_font

def test_asset_manager_singleton(mock_pygame_init):
    """Verifies that AssetManager always returns the same instance."""
    manager1 = AssetManager()
    manager2 = AssetManager()
    assert manager1 is manager2

def test_asset_manager_image_caching(mock_pygame_init):
    """Verifies that images are cached and not loaded twice."""
    mock_load, _ = mock_pygame_init
    manager = AssetManager()
    
    # First call
    img1 = manager.get_image("player/player_stand")
    # Second call
    img2 = manager.get_image("player/player_stand")
    
    assert img1 is img2
    assert mock_load.call_count == 1

def test_asset_manager_font_caching(mock_pygame_init):
    """Verifies that fonts are cached by name and size."""
    _, mock_font = mock_pygame_init
    manager = AssetManager()
    
    f1 = manager.get_font("Arial", 24)
    f2 = manager.get_font("Arial", 24)
    f3 = manager.get_font("Arial", 48) # Different size
    
    assert f1 is f2
    assert f1 is not f3
