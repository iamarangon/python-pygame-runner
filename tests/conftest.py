# tests/conftest.py
import pytest
import pygame
import os

# Set dummy video and audio drivers for headless CI testing before pygame init
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

@pytest.fixture(scope="session", autouse=True)
def pygame_setup():
    try:
        pygame.mixer.init()
    except pygame.error:
        pass  # CI boxes might lack an audio endpoint even with the dummy driver
    pygame.init()
    pygame.font.init()
    # Mocking the display to prevent a window from popping up
    pygame.display.set_mode = lambda *args, **kwargs: pygame.Surface((800, 400))
    pygame.display.flip = lambda: None
    yield
    pygame.quit()
