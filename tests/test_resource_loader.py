import pytest
import pygame
from unittest.mock import patch
from src.core.resource_loader import ResourceLoader


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset ResourceLoader singleton between tests."""
    ResourceLoader._instance = None
    yield
    ResourceLoader._instance = None


class TestResourceLoader:
    def test_get_image_cache_hit(self):
        """Second call to same image returns cached version."""
        rl = ResourceLoader()
        img1 = rl.get_image("Sky.png", "images")
        img2 = rl.get_image("Sky.png", "images")
        assert img1 is img2

    def test_get_image_tuple_scale(self):
        """Passing a tuple scale resizes the image."""
        rl = ResourceLoader()
        img = rl.get_image("Sky.png", "images", scale=(100, 50))
        assert img.get_size() == (100, 50)

    def test_get_image_float_scale(self):
        """Passing a float scale multiplies dimensions."""
        rl = ResourceLoader()
        base = rl.get_image("Sky.png", "images")
        w, h = base.get_size()
        ResourceLoader._instance = None
        rl2 = ResourceLoader()
        scaled = rl2.get_image("Sky.png", "images", scale=0.5)
        assert scaled.get_size() == (int(w * 0.5), int(h * 0.5))

    def test_get_image_missing_returns_fallback(self):
        """Missing image triggers pygame.error and returns a 50x50 fallback surface."""
        rl = ResourceLoader()
        with patch("pygame.image.load", side_effect=pygame.error("not found")):
            result = rl.get_image("nonexistent_image_xyz.png", "images")
        assert result is not None
        assert result.get_size() == (50, 50)

    def test_get_sound_missing_returns_none(self):
        """Missing sound triggers pygame.error and returns None gracefully."""
        rl = ResourceLoader()
        with patch("pygame.mixer.Sound", side_effect=pygame.error("not found")):
            result = rl.get_sound("nonexistent.wav")
        assert result is None

    def test_get_sound_cache_hit(self):
        """Calling get_sound with a pre-cached key returns cached value."""
        import os
        rl = ResourceLoader()
        fake_path = os.path.join(rl.base_path, "sounds", "cached.wav")
        rl.sounds[fake_path] = "CACHED"
        r = rl.get_sound("cached.wav")
        assert r == "CACHED"

    def test_get_font_cache_hit(self):
        """Same font+size returns cached object."""
        rl = ResourceLoader()
        f1 = rl.get_font("Pixeltype.ttf", 36)
        f2 = rl.get_font("Pixeltype.ttf", 36)
        assert f1 is f2

    def test_get_font_missing_returns_sysfont(self):
        """Missing font triggers pygame.error and falls back to SysFont."""
        rl = ResourceLoader()
        with patch("pygame.font.Font", side_effect=pygame.error("not found")):
            font = rl.get_font("nonexistent_font.ttf", 24)
        assert font is not None
