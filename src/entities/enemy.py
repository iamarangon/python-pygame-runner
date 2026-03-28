import pygame
from src.entities.base_entity import GameEntity
from src.assets_manager import AssetManager
from src.constants import SLUG_SIZE, FLY_SIZE, SLUG_SPEED, FLY_SPEED, COLOR_SLUG, COLOR_FLY


class BaseEnemy(GameEntity):
    """
    Common base for all enemies. Moves from right to left with animations.
    """
    def __init__(self, x: float, y: float, width: int, height: int, speed: float, color: tuple):
        super().__init__(x, y, width, height, color)
        self.velocity.x = -speed
        self.assets = AssetManager()
        self.frames = []
        self.animation_index = 0.0
        self.base_animation_speed = 5.0 # Basic FPS

    def update(self, dt: float, animation_multiplier: float = 1.0) -> None:
        """Updates position and animation frame index."""
        self.rect.x += self.velocity.x * dt
        
        # Variable animation speed
        if self.frames:
            self.animation_index += (self.base_animation_speed * animation_multiplier) * dt
            if self.animation_index >= len(self.frames):
                self.animation_index = 0

    def draw(self, screen: pygame.Surface) -> None:
        """Renders the current animation frame."""
        if self.frames:
            current_frame = self.frames[int(self.animation_index)]
            screen.blit(current_frame, self.rect)
        else:
            super().draw(screen)


class Slug(BaseEnemy):
    """
    Ground-level enemy (Snail). 2-frame animation.
    """
    def __init__(self, x: float, y: float, speed: float = SLUG_SPEED):
        super().__init__(x, y, SLUG_SIZE[0], SLUG_SIZE[1], speed, color=COLOR_SLUG)
        
        # Load and scale Snail frames
        self.frames = [
            pygame.transform.scale(self.assets.get_image("snail/snail1"), SLUG_SIZE),
            pygame.transform.scale(self.assets.get_image("snail/snail2"), SLUG_SIZE)
        ]
        
        # Snail is slower
        self.base_animation_speed = 4.0

class Fly(BaseEnemy):
    """
    Aerial enemy. 2-frame animation.
    """
    def __init__(self, x: float, y: float, speed: float = FLY_SPEED):
        super().__init__(x, y, FLY_SIZE[0], FLY_SIZE[1], speed, color=COLOR_FLY)
        
        # Load and scale Fly frames
        self.frames = [
            pygame.transform.scale(self.assets.get_image("fly/fly1"), FLY_SIZE),
            pygame.transform.scale(self.assets.get_image("fly/fly2"), FLY_SIZE)
        ]
        
        # Fly flaps faster
        self.base_animation_speed = 10.0
