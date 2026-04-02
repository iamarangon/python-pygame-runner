# src/core/spawner.py
import random
import pygame
from src.entities.enemies import GroundEnemy, FlyingEnemy
from src.core.settings import SCREEN_WIDTH

PATTERNS: list[list[tuple[str, int]]] = [
    [("ground", 0)],
    [("fly", 0)],
    [("ground", 0), ("ground", 400)],
    [("fly", 0), ("ground", 350)],
    [("ground", 0), ("fly", 450)],
]

class Spawner:
    def __init__(self) -> None:
        self.spawn_timer: int = 0
        self.current_delay: int = 100
        self.enemies: list = []

    def reset(self) -> None:
        self.enemies.clear()
        self.spawn_timer = 0
        self.current_delay = 100

    def get_random_delay(self, phase: int) -> int:
        if phase == 1:
            return random.randint(120, 180)
        elif phase == 2:
            return random.randint(90, 140)
        return random.randint(70, 110)

    def spawn_pattern(self, phase: int) -> None:
        if phase == 1:
            idx = 0
        elif phase == 2:
            idx = random.choice([0, 1, 2])
        else:
            idx = random.randint(0, len(PATTERNS) - 1)

        base_x = SCREEN_WIDTH + 50
        for e_type, offset in PATTERNS[idx]:
            x_pos = base_x + offset
            if e_type == "ground":
                self.enemies.append(GroundEnemy(x_pos))
            elif e_type == "fly":
                self.enemies.append(FlyingEnemy(x_pos))

    def update(self, phase: int, scroll_speed: float, dt: float) -> None:
        self.spawn_timer += 1
        if self.spawn_timer >= self.current_delay:
            self.spawn_pattern(phase)
            self.spawn_timer = 0
            self.current_delay = self.get_random_delay(phase)

        for enemy in self.enemies:
            enemy.update(scroll_speed, dt)

        self.enemies = [e for e in self.enemies if e.rect.right > 0]

    def render(self, surface: pygame.Surface) -> None:
        for enemy in self.enemies:
            enemy.render(surface)
