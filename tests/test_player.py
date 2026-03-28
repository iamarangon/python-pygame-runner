import pytest
import pygame
from unittest.mock import patch, MagicMock
from src.entities.player import Player

@pytest.fixture
def player():
    """Initializes a Player instance for testing with necessary mocks."""
    with patch('pygame.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.image.load', return_value=pygame.Surface((64, 64))), \
         patch('pygame.font'):
        return Player(x=100, y=500)

def test_player_initialization(player):
    """Verifies player initial state."""
    assert player.rect.x == 100
    assert player.rect.y == 500
    assert player.velocity.y == 0
    assert player.is_on_ground is True

def test_player_jump(player):
    """Verifies that jumping sets the correct upward velocity."""
    # Use a dictionary to avoid IndexError with large scancodes
    mock_keys = MagicMock()
    mock_keys.__getitem__.side_effect = lambda k: k == pygame.K_SPACE
    
    with patch('pygame.key.get_pressed', return_value=mock_keys):
        player.handle_input()
        assert player.velocity.y == -900
        assert player.is_on_ground is False

def test_player_crouch(player):
    """Verifies that crouching reduces player height."""
    mock_keys = MagicMock()
    mock_keys.__getitem__.side_effect = lambda k: k == pygame.K_s
    
    with patch('pygame.key.get_pressed', return_value=mock_keys):
        player.handle_input()
        assert player.is_crouching is True
        assert player.rect.height == 32
        assert player.rect.y == 532 # 500 + (64 - 32)

def test_player_gravity_application(player):
    """Verifies that gravity increases downward velocity when not on ground."""
    player.is_on_ground = False
    player.rect.y = 100
    player.velocity.y = 0
    
    # Update with dt = 0.1s
    player.update(0.1)
    assert player.velocity.y == 250
    assert player.rect.y > 100

def test_player_floor_collision(player):
    """Verifies that the player stops at the floor level."""
    player.is_on_ground = False
    player.rect.y = 600
    player.velocity.y = 100
    
    player.update(0.1)
    
    assert player.rect.bottom == 564 # ground_y (500) + original_height (64)
    assert player.velocity.y == 0
    assert player.is_on_ground is True

def test_player_cannot_double_jump(player):
    """Verifies that the player cannot jump while already in the air."""
    player.is_on_ground = False
    player.velocity.y = -100
    
    mock_keys = MagicMock()
    mock_keys.__getitem__.side_effect = lambda k: k == pygame.K_SPACE
    
    with patch('pygame.key.get_pressed', return_value=mock_keys):
        player.handle_input()
        assert player.velocity.y == -100
