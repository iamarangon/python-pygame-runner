import os

# --- Screen Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- File Paths ---
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "data")
ASSETS_PATH = os.path.join(BASE_PATH, "assets")
FONTS_PATH = os.path.join(ASSETS_PATH, "fonts")
IMAGES_PATH = os.path.join(ASSETS_PATH, "graphics")

HIGH_SCORES_FILE = os.path.join(DATA_PATH, "high_scores.json")

# --- Player Physics & Dimensions ---
PLAYER_SIZE = (64, 64)
PLAYER_CROUCH_HEIGHT = 32
PLAYER_GRAVITY = 2500
PLAYER_JUMP_VELOCITY = -900
PLAYER_START_X = 100
PLAYER_GROUND_Y = 560 - PLAYER_SIZE[1] # Align bottom to ground line (560)

# --- Enemy Configuration ---
SLUG_SIZE = (48, 32)
FLY_SIZE = (48, 48)

SLUG_SPEED = 200
FLY_SPEED = 350

# Fly Spawning Heights
FLY_HEIGHT_HEAD = SCREEN_HEIGHT - 130  # Crouch required (approx 470)
FLY_HEIGHT_HIGH = SCREEN_HEIGHT - 220  # Jump obstacle (approx 380)

# --- Spawning & Difficulty ---
INITIAL_SPAWN_INTERVAL = 2.0
MIN_SPAWN_INTERVAL = 0.5
SPAWN_REDUCTION_SCORE_STEP = 500
SPAWN_REDUCTION_AMOUNT = 0.1

SCORE_TICK_RATE = 10  # Points per second
PARALLAX_BASE_SPEED = 200 # Constant world scroll speed

# --- UI & Layout ---
MAX_NAME_LENGTH = 10

# --- Colors (RGB) ---
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GOLD = (255, 215, 0)
COLOR_SILVER = (192, 192, 192)
COLOR_BRONZE = (205, 127, 50)
COLOR_GREY = (80, 80, 80)
COLOR_LIGHT_GREY = (200, 200, 200)

COLOR_FOREST_BG = (40, 60, 20)
COLOR_MENU_BG = (20, 40, 60)
COLOR_GAMEOVER_BG = (30, 10, 10)
COLOR_NAMING_BG = (20, 20, 30)

COLOR_DANGER_RED = (255, 50, 50)
COLOR_UI_PLAYER = (0, 128, 255)
COLOR_SLUG = (100, 200, 100)
COLOR_FLY = (200, 100, 200)

# --- Overlay Configuration ---
PAUSE_OVERLAY_ALPHA = 150
