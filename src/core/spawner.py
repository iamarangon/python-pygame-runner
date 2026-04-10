# src/core/spawner.py
import random
import pygame
from src.entities.enemies import GroundEnemy, FlyingEnemy
from src.core.settings import SCREEN_WIDTH, SPAWN_INTERVAL_P1, SPAWN_INTERVAL_P2, SPAWN_INTERVAL_P3

PATTERNS: list[list[tuple[str, int]]] = [
    [("ground", 0)],
    [("fly", 0)],
    [("ground", 0), ("ground", 400)],
    [("fly", 0), ("ground", 350)],
    [("ground", 0), ("fly", 450)],
]

class Spawner:
    def get_dynamic_interval(self, phase: int) -> int:
        if phase == 1:
            return SPAWN_INTERVAL_P1
        elif phase == 2:
            return SPAWN_INTERVAL_P2
        return SPAWN_INTERVAL_P3

    def spawn(self, phase: int, group: pygame.sprite.Group) -> None:
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
                group.add(GroundEnemy(x_pos))
            elif e_type == "fly":
                group.add(FlyingEnemy(x_pos))
