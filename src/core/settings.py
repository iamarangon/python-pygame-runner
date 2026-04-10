# src/core/settings.py

SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 400
FPS: int = 60

TARGET_FPS: int = 60

COLORS: dict[str, tuple[int, ...]] = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 50, 50),
    "dark_red": (180, 0, 0),
    "green": (50, 255, 50),
    "blue": (50, 50, 255),
    "ground": (50, 150, 50),
    "sky": (135, 206, 235),
    "text": (240, 240, 240),
    "text_dark": (30, 30, 30),
    "yellow": (255, 220, 0),
    "overlay": (0, 0, 0, 128)
}

GRAVITY: float = 0.5
JUMP_STRENGTH: float = -12.0
FAST_FALL_STRENGTH: float = 2.0
BASE_SCROLL_SPEED: float = 5.0
MAX_SCROLL_SPEED: float = 12.0

GROUND_Y: int = 320

PAUSE_COUNTDOWN: float = 3.0
SPAWN_INTERVAL_P1: int = 1500
SPAWN_INTERVAL_P2: int = 1100
SPAWN_INTERVAL_P3: int = 800
VOLUME_LEVELS: int = 4
DIFFICULTY_LEVELS: list[str] = ["Easy", "Normal", "Hard"]
