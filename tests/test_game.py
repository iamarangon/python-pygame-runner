import pytest
import pygame
from src.core.game import Game
from src.states.state import State

class DummyState(State):
    def __init__(self, game):
        super().__init__(game)
        self.updated = False
        self.rendered = False
        self.handled = False
        
    def update(self, dt):
        self.updated = True
        
    def render(self, surface):
        self.rendered = True
        
    def handle_events(self, events):
        self.handled = True

def test_game_loop():
    game = Game()
    game.load_states()
    
    assert game.running is True
    
    dummy = DummyState(game)
    game.state_stack.append(dummy)
    
    game.update(0.16)
    assert dummy.updated is True
    
    # We can't render cleanly without Pygane context crash, but we can verify events
    game.handle_events()
    
    # Simulate Quit
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    game.handle_events()
    assert game.running is False
