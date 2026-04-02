# src/entities/background.py
import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, COLORS
from src.core.resource_loader import ResourceLoader

class Background:
    def __init__(self) -> None:
        rl = ResourceLoader()
        self.sky_surf: pygame.Surface = rl.get_image(
            "Sky.png", "images", scale=(SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        raw_ground = rl.get_image("ground.png", "images")
        ground_height = SCREEN_HEIGHT - GROUND_Y
        self.ground_surf: pygame.Surface = pygame.transform.scale(
            raw_ground, (SCREEN_WIDTH, ground_height)
        )

        self.sky_x1: int = 0
        self.sky_x2: int = SCREEN_WIDTH
        self.ground_x1: int = 0
        self.ground_x2: int = SCREEN_WIDTH

    def update_sky(self, scroll_speed: float, dt: float) -> None:
        self.sky_x1 -= scroll_speed * 0.5
        self.sky_x2 -= scroll_speed * 0.5

        if self.sky_x1 <= -SCREEN_WIDTH:
            self.sky_x1 = self.sky_x2 + SCREEN_WIDTH
        if self.sky_x2 <= -SCREEN_WIDTH:
            self.sky_x2 = self.sky_x1 + SCREEN_WIDTH

    def update_ground(self, scroll_speed: float, dt: float) -> None:
        self.ground_x1 -= int(scroll_speed)
        self.ground_x2 -= int(scroll_speed)

        if self.ground_x1 <= -SCREEN_WIDTH:
            self.ground_x1 = self.ground_x2 + SCREEN_WIDTH
        if self.ground_x2 <= -SCREEN_WIDTH:
            self.ground_x2 = self.ground_x1 + SCREEN_WIDTH

    def update(self, scroll_speed: float, dt: float) -> None:
        self.update_sky(scroll_speed, dt)
        self.update_ground(scroll_speed, dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.sky_surf, (self.sky_x1, 0))
        surface.blit(self.sky_surf, (self.sky_x2, 0))
        surface.blit(self.ground_surf, (self.ground_x1, GROUND_Y))
        surface.blit(self.ground_surf, (self.ground_x2, GROUND_Y))
