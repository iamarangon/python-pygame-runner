# tests/conftest.py
import pytest
import pygame
import os

# Set dummy video driver for headless testing before pygame init
# Sometimes SDL_VIDEODRIVER isn't enough depending on OS, but we also mock display
os.environ["SDL_VIDEODRIVER"] = "dummy"

@pytest.fixture(scope="session", autouse=True)
def pygame_setup():
    pygame.mixer.init()
    pygame.init()
    pygame.font.init()
    # Mocking the display to prevent a window from popping up
    pygame.display.set_mode = lambda *args, **kwargs: pygame.Surface((800, 400))
    pygame.display.flip = lambda: None
    yield
    pygame.quit()
