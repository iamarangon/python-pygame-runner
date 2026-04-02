import pytest
from src.core.spawner import Spawner

def test_spawner_initialization():
    spawner = Spawner()
    assert spawner.spawn_timer == 0
    assert len(spawner.enemies) == 0

def test_spawner_spawn_pattern():
    spawner = Spawner()
    
    # Force phase 1 (spawn ground only)
    spawner.spawn_pattern(1)
    
    assert len(spawner.enemies) == 1
    # Check if instance is GroundEnemy
    from src.entities.enemies import GroundEnemy
    assert isinstance(spawner.enemies[0], GroundEnemy)

def test_spawner_update():
    spawner = Spawner()
    # Mock current delay to 10 to trigger it fast
    spawner.current_delay = 10
    spawner.spawn_timer = 9
    
    spawner.update(1, 5.0, 0.016)
    
    # Should have triggered spawn pattern and reset timer
    assert spawner.spawn_timer == 0
    assert len(spawner.enemies) == 1

def test_spawner_cleanup():
    spawner = Spawner()
    spawner.spawn_pattern(1)
    enemy = spawner.enemies[0]
    
    # Move enemy extremely left to force cleanup
    enemy.x = -100
    
    spawner.update(1, 5.0, 0.016) # Trigger update which contains off-screen check
    
    assert len(spawner.enemies) == 0
