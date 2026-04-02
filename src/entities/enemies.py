# src/entities/enemies.py
import pygame
from src.core.settings import GROUND_Y, COLORS
from src.core.resource_loader import ResourceLoader

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: float) -> None:
        super().__init__()
        self.x: float = x
        self.y: float = y
        self.speed: float = speed
        self.frames: list[pygame.Surface] = []
        self.frame_index: float = 0.0
        self.image: pygame.Surface | None = None
        self.rect: pygame.Rect | None = None
        self.animation_speed: float = 5.0

    def setup_rect(self) -> None:
        if self.frames:
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def update(self, scroll_speed: float, dt: float) -> None:
        self.x -= self.speed + scroll_speed

        if self.frames:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

        if self.rect:
            self.rect.x = int(self.x)

    def render(self, surface: pygame.Surface) -> None:
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, COLORS["red"], self.rect)


class GroundEnemy(Enemy):
    def __init__(self, x: int) -> None:
        super().__init__(x, y=0, speed=0.0)
        rl = ResourceLoader()
        self.frames = [
            rl.get_image("snail1.png", "images/snail"),
            rl.get_image("snail2.png", "images/snail"),
        ]
        self.animation_speed = 4.0
        self.image = self.frames[0]
        self.y = GROUND_Y - self.image.get_height()
        self.setup_rect()


class FlyingEnemy(Enemy):
    def __init__(self, x: int) -> None:
        super().__init__(x, y=GROUND_Y - 95, speed=1.0)
        rl = ResourceLoader()
        self.frames = [
            rl.get_image("fly1.png", "images/fly"),
            rl.get_image("fly2.png", "images/fly"),
        ]
        self.animation_speed = 10.0
        self.image = self.frames[0]
        self.setup_rect()
