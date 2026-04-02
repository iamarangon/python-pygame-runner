import pygame
import pytest
from src.core.game import Game
from src.states.options_state import OptionsState

def test_options_navigation():
    game = Game()
    options = OptionsState(game)
    
    options.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)])
    assert options.selected_index == 1
    
    options.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)])
    assert options.selected_index == 2
    
    # Should pop state
    game.state_stack.append(options)
    options.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
    assert len(game.state_stack) == 0

def test_options_tweaks():
    game = Game()
    options = OptionsState(game)
    
    # Select Volume
    options.selected_index = 0
    
    # Hit Left
    game.config.volume = 2
    options.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)])
    assert game.config.volume == 1
    
    # Hit Right
    options.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)])
    assert game.config.volume == 2
    
    # Select Diff
    options.selected_index = 1
    game.config.difficulty = "Normal"
    # Right
    options.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)])
    assert game.config.difficulty == "Hard"
    
    # Left
    options.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)])
    assert game.config.difficulty == "Normal"
