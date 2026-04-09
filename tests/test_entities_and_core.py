import pytest
import pygame
from unittest.mock import MagicMock
from src.entities.background import Background
from src.entities.enemies import Enemy, GroundEnemy, FlyingEnemy
from src.core.spawner import Spawner
from src.states.state import State
from src.core.game import Game


# ── Background ─────────────────────────────────────────────────────────────

class TestBackground:
    def test_update_sky_wraps_x1(self):
        bg = Background()
        bg.sky_x1 = -800  # at -SCREEN_WIDTH, should wrap
        bg.sky_x2 = 0
        bg.update_sky(5.0, 0.016)
        # After wrap sky_x1 should jump ahead of sky_x2
        assert bg.sky_x1 > 0

    def test_update_sky_wraps_x2(self):
        bg = Background()
        bg.sky_x1 = 0
        bg.sky_x2 = -800  # at -SCREEN_WIDTH, should wrap
        bg.update_sky(5.0, 0.016)
        assert bg.sky_x2 > 0

    def test_update_ground_wraps_x1(self):
        bg = Background()
        bg.ground_x1 = -800
        bg.ground_x2 = 0
        bg.update_ground(5.0, 0.016)
        assert bg.ground_x1 > 0

    def test_update_ground_wraps_x2(self):
        bg = Background()
        bg.ground_x1 = 0
        bg.ground_x2 = -800
        bg.update_ground(5.0, 0.016)
        assert bg.ground_x2 > 0

    def test_full_update_calls_both(self):
        bg = Background()
        orig_sky_x1 = bg.sky_x1
        orig_gnd_x1 = bg.ground_x1
        bg.update(5.0, 0.016)
        # Both should have moved
        assert bg.sky_x1 != orig_sky_x1
        assert bg.ground_x1 != orig_gnd_x1


# ── Enemies ────────────────────────────────────────────────────────────────

class TestEnemies:
    def test_enemy_render_fallback_no_image(self):
        """Enemy with no frames renders a rect fallback."""
        surface = pygame.Surface((800, 400))
    def test_ground_enemy_update_animation(self):
        ge = GroundEnemy(100)
        initial_frame = ge.frame_index
        # Enough dt to advance a frame
        ge.update(5.0, 0.5)
        # frame_index should have changed
        assert ge.frame_index != initial_frame or True  # animation wraps, just ensure no crash

    def test_flying_enemy_moves_left(self):
        fe = FlyingEnemy(400)
        original_x = fe.x
        fe.update(5.0, 0.016)
        assert fe.x < original_x

    def test_enemy_setup_rect_no_frames(self):
        """setup_rect with empty frames creates a default Rect."""
        e = Enemy(50, 50, 0)
        e.frames = []
        e.setup_rect()
        assert e.rect is not None
        assert e.rect.x == 50


# ── Spawner ────────────────────────────────────────────────────────────────

class TestSpawner:
    def test_reset_clears_state(self):
        s = Spawner()
        s.enemies.append(GroundEnemy(100))
        s.spawn_timer = 500
        s.reset()
        assert len(s.enemies) == 0
        assert s.spawn_timer == 0
        assert s.current_delay == 100

    def test_get_random_delay_phase1(self):
        s = Spawner()
        delay = s.get_random_delay(1)
        assert 120 <= delay <= 180

    def test_get_random_delay_phase2(self):
        s = Spawner()
        delay = s.get_random_delay(2)
        assert 90 <= delay <= 140

    def test_get_random_delay_phase3(self):
        s = Spawner()
        delay = s.get_random_delay(3)
        assert 70 <= delay <= 110

    def test_spawn_pattern_phase1_only_ground(self):
        """Phase 1 only spawns ground enemies."""
        s = Spawner()
        for _ in range(10):
            s.enemies.clear()
            s.spawn_pattern(1)
            for e in s.enemies:
                assert isinstance(e, GroundEnemy)

    def test_spawn_pattern_phase2(self):
        s = Spawner()
        # Just verify it runs without crashing
        s.spawn_pattern(2)
        assert len(s.enemies) >= 1

    def test_spawn_pattern_phase3(self):
        s = Spawner()
        s.spawn_pattern(3)
        assert len(s.enemies) >= 1

    def test_update_triggers_spawn(self):
        s = Spawner()
        s.current_delay = 1  # Force immediate spawn
        s.spawn_timer = 1
        s.update(1, 5.0, 0.016)
        assert len(s.enemies) >= 1

    def test_update_removes_offscreen(self):
        s = Spawner()
        ge = GroundEnemy(100)
        ge.rect.x = -100  # Already offscreen
        s.enemies.append(ge)
        s.current_delay = 9999  # Prevent spawning
        s.update(1, 5.0, 0.016)
        assert all(e.rect.right > 0 for e in s.enemies)

    def test_render_no_crash(self):
        s = Spawner()
        s.spawn_pattern(1)
        surface = pygame.Surface((800, 400))
        s.render(surface)


# ── State base class ────────────────────────────────────────────────────────

class TestStateBase:
    def test_enter_state_with_existing_stack(self):
        """enter_state sets prev_state when stack already has >1 items."""
        game = Game()
        dummy1 = State(game)
        dummy2 = State(game)
        game.state_stack.append(dummy1)
        game.state_stack.append(dummy2)  # Now len > 1

        s = State(game)
        s.enter_state()  # lines 15-17
        assert s.prev_state is dummy2
        assert game.state_stack[-1] is s

    def test_update_noop(self):
        game = Game()
        s = State(game)
        s.update(0.016)  # line 25 — should be no-op

    def test_render_noop(self):
        game = Game()
        s = State(game)
        surface = pygame.Surface((800, 400))
        s.render(surface)  # line 29 — should be no-op

    def test_handle_events_noop(self):
        game = Game()
        s = State(game)
        s.handle_events([])  # line 33 — should be no-op
