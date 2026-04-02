# src/core/settings.py

# Display configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

# Frame independent timing (delta time factor) assumes base 60 FPS
TARGET_FPS = 60

# Colors for placeholder graphics and UI
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 50, 50),        # Flying Enemies
    "dark_red": (180, 0, 0),    # Ground Enemies
    "green": (50, 255, 50),     # Player
    "blue": (50, 50, 255),
    "ground": (50, 150, 50),    # Floor
    "sky": (135, 206, 235),     # BG
    "text": (240, 240, 240),
    "text_dark": (30, 30, 30),
    "yellow": (255, 220, 0),
    "overlay": (0, 0, 0, 128)
}

# Physics Settings
GRAVITY = 0.5
JUMP_STRENGTH = -12.0
FAST_FALL_STRENGTH = 2.0
BASE_SCROLL_SPEED = 5.0
MAX_SCROLL_SPEED = 12.0

# Layout
GROUND_Y = 320 # The Y coordinate where entities rest
