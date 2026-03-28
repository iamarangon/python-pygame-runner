import pygame
from abc import ABC, abstractmethod

class GameEntity(ABC):
    """
    Abstract base class for all game objects (Player, Enemies, Obstacles).
    Provides core functionality for position, physics, and rendering.
    """
    def __init__(self, x: float, y: float, width: int, height: int, color: tuple = (255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.velocity = pygame.Vector2(0, 0)
        self.is_on_ground = False

    @abstractmethod
    def update(self, dt: float) -> None:
        """Updates entity logic. Must be implemented by subclasses."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Renders the entity (placeholder rectangle) to the screen."""
        pygame.draw.rect(screen, self.color, self.rect)

    def apply_gravity(self, gravity: float, dt: float) -> None:
        """Applies downward force to the entity's velocity."""
        if not self.is_on_ground:
            self.velocity.y += gravity * dt
        else:
            self.velocity.y = 0
