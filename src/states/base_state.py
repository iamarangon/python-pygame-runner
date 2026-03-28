from abc import ABC, abstractmethod
import pygame


class BaseState(ABC):
    """
    Abstract base class for all game states (scenes).
    Provides a consistent interface for the StateManager.
    """
    def __init__(self, state_manager):
        self.manager = state_manager

    def on_enter(self) -> None:
        """
        Logic to execute when the state becomes active. 
        Optional for subclasses to implement.
        """
        pass

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Processes events specific to this state."""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """Updates the logic of the state."""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Renders the state to the screen."""
        pass
