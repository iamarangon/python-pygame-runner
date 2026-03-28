import pygame
import os
from src.constants import ASSETS_PATH, FONTS_PATH, IMAGES_PATH


class AssetManager:
    """
    Singleton utility to manage, cache, and provide game resources 
    (images, fonts, sounds) throughout the application lifecycle.
    """
    _instance = None

    def __new__(cls):
        """Standard Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Configures resource base paths and initializes caches."""
        if self._initialized:
            return
            
        # Resource base paths from centralized constants
        self.base_path = ASSETS_PATH
        self.fonts_path = FONTS_PATH
        self.images_path = IMAGES_PATH
        
        # In-memory caches
        self.images = {}
        self.fonts = {}
        self.sounds = {}
        
        self._initialized = True
        print(f"[AssetManager] Base path initialized at: {self.base_path}")

    def get_image(self, name: str, alpha: bool = True) -> pygame.Surface:
        """
        Loads and returns a cached image. 
        Supports subfolders via path-like names (e.g. 'player/player_stand').
        """
        if name not in self.images:
            # Join images_path with the name, then add .png
            path = os.path.join(self.images_path, f"{name}.png")
            try:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Image not found at {path}")
                
                image = pygame.image.load(path)
                if alpha:
                    image = image.convert_alpha()
                else:
                    image = image.convert()
                self.images[name] = image
            except (pygame.error, FileNotFoundError) as e:
                print(f"[AssetManager] Error loading image {name}: {e}")
                # Return a small placeholder surface if failed
                placeholder = pygame.Surface((32, 32))
                placeholder.fill((255, 0, 255)) # Generic Magenta error color
                self.images[name] = placeholder
                
        return self.images[name]

    def get_font(self, name: str, size: int) -> pygame.font.Font:
        """Loads and returns a cached font. Falls back to Pixeltype or Arial if not found."""
        key = f"{name}_{size}"
        if key not in self.fonts:
            path = os.path.join(self.fonts_path, f"{name}.ttf")
            try:
                if os.path.exists(path):
                    font = pygame.font.Font(path, size)
                else:
                    # Fallback to Pixeltype if it exists in assets
                    pixel_path = os.path.join(self.fonts_path, "Pixeltype.ttf")
                    if os.path.exists(pixel_path):
                        font = pygame.font.Font(pixel_path, size)
                    else:
                        font = pygame.font.SysFont("Arial", size)
                self.fonts[key] = font
            except pygame.error as e:
                print(f"[AssetManager] Error loading font {name}: {e}")
                self.fonts[key] = pygame.font.SysFont("Arial", size)
                
        return self.fonts[key]
