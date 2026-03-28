from enum import Enum, auto


class GameState(Enum):
    """
    Available states for the game engine.
    Used by the StateManager to transition between scenes.
    """
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    NAMING = auto()
    GAME_OVER = auto()
