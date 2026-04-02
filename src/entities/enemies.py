# src/entities/enemies.py
import pygame
from src.core.settings import SCREEN_WIDTH, GROUND_Y, COLORS
from src.core.resource_loader import ResourceLoader

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.frames = []
        self.frame_index = 0
        self.image = None
        self.rect = None
        self.animation_speed = 5.0

    def setup_rect(self):
        if self.frames:
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def update(self, scroll_speed, dt):
        self.x -= (self.speed + scroll_speed)
        
        # Animate
        if self.frames:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]
            
        if self.rect:
            self.rect.x = int(self.x)

    def render(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, COLORS["red"], self.rect)
        
class GroundEnemy(Enemy):
    def __init__(self, x):
        super().__init__(x, y=0, speed=0.0)
        rl = ResourceLoader()
        self.frames = [
            rl.get_image("snail1.png", "images/snail"),
            rl.get_image("snail2.png", "images/snail")
        ]
        self.animation_speed = 4.0
        self.image = self.frames[0]
        self.y = GROUND_Y - self.image.get_height()
        self.setup_rect()

class FlyingEnemy(Enemy):
    def __init__(self, x):
        super().__init__(x, y=GROUND_Y - 95, speed=1.0) # Hover higher to force duck
        rl = ResourceLoader()
        self.frames = [
            rl.get_image("fly1.png", "images/fly"),
            rl.get_image("fly2.png", "images/fly")
        ]
        self.animation_speed = 10.0
        self.image = self.frames[0]
        self.setup_rect()
