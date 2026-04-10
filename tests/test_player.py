import pygame
import pytest
from src.entities.player import Player
from src.core.settings import GROUND_Y, JUMP_STRENGTH, GRAVITY

def test_player_initialization():
    player = Player()
    assert player.is_jumping is False
    assert player.is_ducking is False
    assert player.rect.bottom == GROUND_Y
    assert player.rect.height == player.height_stand

def test_player_jump():
    player = Player()
    
    # Simulate pressing UP key
    keys = {pygame.K_UP: True, pygame.K_SPACE: False, pygame.K_DOWN: False}
    player.handle_input(keys)
    
    assert player.is_jumping is True
    assert player.velocity_y == JUMP_STRENGTH
    
    # Check that another jump key doesn't trigger double jump if no condition
    player.handle_input(keys)
    assert player.velocity_y == JUMP_STRENGTH # Should remain unchanged initially

def test_player_duck():
    player = Player()

    keys = {pygame.K_UP: False, pygame.K_SPACE: False, pygame.K_DOWN: True}
    player.handle_input(keys)
    player.update(0.016)

    assert player.is_ducking is True
    assert player.rect.height == player.duck_frames[0].get_height()
    assert player.rect.bottom == GROUND_Y

def test_player_fast_fall():
    player = Player()
    player.is_jumping = True
    player.velocity_y = 0.0

    keys = {pygame.K_UP: False, pygame.K_SPACE: False, pygame.K_DOWN: True}
    player.handle_input(keys)

    assert player.is_ducking is False
    assert player.velocity_y > 0.0

def test_player_update_gravity():
    player = Player()
    player.is_jumping = True
    player.velocity_y = JUMP_STRENGTH
    player.rect.y -= 50

    initial_y = player.rect.y
    initial_vel = player.velocity_y

    player.update(0.016)

    assert player.velocity_y == initial_vel + GRAVITY
    assert player.rect.y == initial_y + int(player.velocity_y)

def test_player_ground_collision():
    player = Player()
    player.rect.bottom = GROUND_Y + 20
    player.velocity_y = 5.0
    player.is_jumping = True

    player.update(0.016)

    assert player.rect.bottom == GROUND_Y
    assert player.velocity_y == 0
    assert player.is_jumping is False
