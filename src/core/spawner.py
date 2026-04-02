# src/core/spawner.py
import random
from src.entities.enemies import GroundEnemy, FlyingEnemy
from src.core.settings import SCREEN_WIDTH

class Spawner:
    def __init__(self):
        self.spawn_timer = 0
        self.current_delay = 100 # Frames until next spawn
        self.enemies = []
        
        # Patterns (List of tuples. Each tuple is a set of enemies to spawn sequentially with small offsets)
        # e.g. "ground_single", "fly_single", "ground_double", "fly_then_ground"
        self.patterns = [
            [("ground", 0)],
            [("fly", 0)],
            [("ground", 0), ("ground", 400)], # Double jump gap
            [("fly", 0), ("ground", 350)],    # Duck then jump
            [("ground", 0), ("fly", 450)]     # Jump then duck
        ]

    def reset(self):
        self.enemies.clear()
        self.spawn_timer = 0
        self.current_delay = 100

    def get_random_delay(self, phase):
        # Adaptive delay based on phase 
        # Phase 1: 0-30s
        # Phase 2: 30-60s
        # Phase 3: 60s+
        if phase == 1:
            return random.randint(120, 180) # Slower spawns
        elif phase == 2:
            return random.randint(90, 140)
        else:
            # Phase 3: Chaos, but ensure at least 70 frames to avoid impossible clumps
            return random.randint(70, 110)

    def spawn_pattern(self, phase):
        # Pick a pattern based on phase. Harder patterns unlock in later phases.
        if phase == 1:
            idx = random.choice([0]) # Only single ground enemies in phase 1 
        elif phase == 2:
            idx = random.choice([0, 1, 2]) # Single ground, single fly, double ground
        else:
            idx = random.randint(0, len(self.patterns) - 1)
            
        pattern = self.patterns[idx]
        
        base_x = SCREEN_WIDTH + 50
        for e_type, offset in pattern:
            x_pos = base_x + offset
            if e_type == "ground":
                self.enemies.append(GroundEnemy(x_pos))
            elif e_type == "fly":
                self.enemies.append(FlyingEnemy(x_pos))

    def update(self, phase, scroll_speed, dt):
        self.spawn_timer += 1
        if self.spawn_timer >= self.current_delay:
            self.spawn_pattern(phase)
            self.spawn_timer = 0
            self.current_delay = self.get_random_delay(phase)

        # Update existing enemies
        for enemy in self.enemies:
            enemy.update(scroll_speed, dt)
            
        # Remove off-screen enemies
        self.enemies = [e for e in self.enemies if e.rect.right > 0]
        
    def render(self, surface):
        for enemy in self.enemies:
            enemy.render(surface)
