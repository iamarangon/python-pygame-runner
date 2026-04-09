import pytest
import pygame
from src.core.spawner import Spawner
from src.entities.enemies import GroundEnemy, FlyingEnemy

def test_spawner_get_dynamic_interval():
    spawner = Spawner()
    assert spawner.get_dynamic_interval(1) == 1500
    assert spawner.get_dynamic_interval(2) == 1100
    assert spawner.get_dynamic_interval(3) == 800

def test_spawner_spawn_phase_1():
    spawner = Spawner()
    group = pygame.sprite.Group()
    
    # Phase 1 only spawns Ground patterns
    spawner.spawn(1, group)
    assert len(group.sprites()) == 1
    assert isinstance(group.sprites()[0], GroundEnemy)

def test_spawner_spawn_phase_2():
    spawner = Spawner()
    group = pygame.sprite.Group()
    
    # Phase 2 spawns from patterns 0, 1, 2
    spawner.spawn(2, group)
    assert 1 <= len(group.sprites()) <= 2
    for sprite in group.sprites():
        assert isinstance(sprite, (GroundEnemy, FlyingEnemy))

def test_spawner_spawn_phase_3():
    spawner = Spawner()
    group = pygame.sprite.Group()
    
    # Phase 3 spawns any pattern
    spawner.spawn(3, group)
    assert 1 <= len(group.sprites()) <= 2
    for sprite in group.sprites():
        assert isinstance(sprite, (GroundEnemy, FlyingEnemy))
