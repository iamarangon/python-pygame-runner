import pytest
import pygame
from src.core.game import Game
from src.states.menu_state import MenuState
from src.states.play_state import PlayState
from src.states.leaderboard_state import LeaderboardState
from src.states.pause_state import PauseState

def test_menu_navigation():
    game = Game()
    menu = MenuState(game)
    
    assert menu.selected_index == 0
    
    # Down Arrow
    menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)])
    assert menu.selected_index == 1
    
    # Up Arrow twice to wrap around
    menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)])
    menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)])
    assert menu.selected_index == 3

def test_menu_transition_to_play():
    game = Game()
    menu = MenuState(game)
    menu.enter_state()
    
    menu.selected_index = 0
    menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
    
    assert isinstance(game.state_stack[-1], PlayState)

def test_pause_countdown():
    game = Game()
    play = PlayState(game)
    play.enter_state()
    
    pause = PauseState(game)
    pause.enter_state()
    
    assert pause.resume_timer == -1
    
    pause.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)])
    assert pause.resume_timer == 3.0
    
    pause.update(3.1) # Simulate 3.1 seconds passing
    
    # Pause should exit itself
    assert game.state_stack[-1] == play
