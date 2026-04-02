# src/states/state.py

class State:
    """
    Base class for all game states.
    Each state should inherit from this and implement the basic methods.
    """
    def __init__(self, game):
        # Reference to the main Game class to access the screen, font, states, etc.
        self.game = game 
        self.prev_state = None

    def enter_state(self):
        """Called when the state becomes active."""
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        """Called to remove the state and go back to the previous one."""
        self.game.state_stack.pop()

    def update(self, dt):
        """Update state logic. 'dt' is delta time."""
        pass

    def render(self, surface):
        """Render state graphics."""
        pass
        
    def handle_events(self, events):
        """Process pygame events."""
        pass
