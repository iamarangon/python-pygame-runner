import pytest
import pygame
from src.core.game import Game
from src.states.menu_state import MenuState
from src.states.play_state import PlayState
from src.states.leaderboard_state import LeaderboardState
from src.states.pause_state import PauseState
from src.states.game_over_state import GameOverState
from src.states.naming_state import NamingState

@pytest.fixture
def dummy_surface():
    return pygame.Surface((800, 400))

def test_full_state_rendering(dummy_surface):
    game = Game()
    
    # Menu State
    menu = MenuState(game)
    menu.update(0.16)
    menu.render(dummy_surface)
    
    # Options State
    from src.states.options_state import OptionsState
    opts = OptionsState(game)
    opts.update(0.16)
    opts.render(dummy_surface)
    
    # Leaderboard State
    lb = LeaderboardState(game)
    lb.update(0.16)
    lb.render(dummy_surface)
    
    # Play State
    play = PlayState(game)
    play.update(0.16)
    play.render(dummy_surface)
    
    # Pause State
    pause = PauseState(game)
    pause.resume_timer = 2.0
    pause.render(dummy_surface)
    pause.resume_timer = -1
    pause.render(dummy_surface)
    
    # Game Over
    go = GameOverState(game, 500)
    go.update(0.16)
    go.render(dummy_surface)
    
    # Naming State
    name = NamingState(game, 500)
    name.update(0.16)
    name.name = "ABC"
    name.render(dummy_surface)

def test_play_state_collisions(dummy_surface, monkeypatch):
    game = Game()
    play = PlayState(game)
    # Mock spawner to create a collision
    play.spawner.spawn_pattern(1)
    play.spawner.enemies[0].rect = play.player.rect.copy()
    
    play.check_collisions()
    
    # This should transition to game over
    assert isinstance(game.state_stack[-1], GameOverState)
    
def test_game_loop_methods(dummy_surface):
    game = Game()
    game.load_states()
    game.update(0.16)
    game.render()

def test_game_over_events():
    game = Game()
    go = GameOverState(game, 99999) # Top score
    
    # Hit enter
    go.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)])
    
    # Should pop into naming
    assert isinstance(game.state_stack[-1], NamingState)

    
def test_naming_state_events():
    game = Game()
    name = NamingState(game, 99999)
    name.enter_state()  # add state to stack
    # Type A
    name.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a, unicode="a")])
    assert name.name == "A"
    
    # Backspace
    name.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE)])
    assert name.name == ""
    
    # Submit empty
    name.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
    
