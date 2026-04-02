import pytest
import pygame
from src.core.game import Game
from src.states.play_state import PlayState

def test_play_state_phases():
    game = Game()
    play = PlayState(game)
    
    # Phase 1
    play.update(10.0) # timer = 10
    assert play.phase == 1
    
    # Phase 2
    play.update(30.0) # timer = 40
    assert play.phase == 2
    
    # Phase 3
    play.update(30.0) # timer = 70
    assert play.phase == 3

def test_play_state_pause():
    game = Game()
    play = PlayState(game)
    game.state_stack.append(play)
    
    play.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)])
    assert len(game.state_stack) == 2
    assert type(game.state_stack[-1]).__name__ == "PauseState"
