from src.state_enums import GameState
from src.shared_state import GameSession
from src.states.menu_state import MenuState
from src.states.play_state import PlayState
from src.states.game_over_state import GameOverState
from src.states.pause_state import PauseState
from src.states.naming_state import NamingState


class StateManager:
    """
    Manages transitions between game states and handles 
    state-specific logic and rendering using the State Pattern.
    """

    def __init__(self, initial_state: GameState = GameState.MENU):
        self.session = GameSession()
        self._current_state_enum = initial_state
        self._states = {
            GameState.MENU: MenuState(self),
            GameState.PLAYING: PlayState(self),
            GameState.PAUSED: PauseState(self),
            GameState.NAMING: NamingState(self),
            GameState.GAME_OVER: GameOverState(self)
        }
        self._active_state = self._states[self._current_state_enum]
        self._active_state.on_enter() # Initialize initial state

    @property
    def current_state(self) -> GameState:
        """Read-only access to the current state type (Enum)."""
        return self._current_state_enum

    def change_state(self, new_state: GameState) -> None:
        """Transitions to a new state and updates the active handler."""
        if new_state in self._states:
            # Exit previous state logic
            if hasattr(self._active_state, "on_exit"):
                self._active_state.on_exit()
                
            self._current_state_enum = new_state
            self._active_state = self._states[new_state]
            self._active_state.on_enter() # Refresh state data

    def handle_events(self, events: list) -> None:
        """Delegates event processing to the active state."""
        self._active_state.handle_events(events)

    def update(self, dt: float) -> None:
        """Delegates logic update to the active state."""
        self._active_state.update(dt)

    def draw(self, screen) -> None:
        """Delegates rendering to the active state."""
        self._active_state.draw(screen)
