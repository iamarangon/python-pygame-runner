# src/core/resource_loader.py
import pygame
import os
import sys

class ResourceLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceLoader, cls).__new__(cls)
            cls._instance.images = {}
            cls._instance.sounds = {}
            cls._instance.fonts = {}

            if hasattr(sys, '_MEIPASS'):
                base_dir = sys._MEIPASS
            else:
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

            cls._instance.base_path = os.path.join(base_dir, 'assets')
        return cls._instance

    def get_image(self, name: str, subfolder: str = "images", scale: tuple[int, int] | float | None = None) -> pygame.Surface:
        path = os.path.join(self.base_path, subfolder, name)

        if path in self.images:
            return self.images[path]

        try:
            image = pygame.image.load(path)
            if pygame.display.get_surface():
                image = image.convert_alpha()

            if scale:
                if isinstance(scale, tuple):
                    image = pygame.transform.scale(image, scale)
                elif isinstance(scale, (float, int)):
                    size = image.get_size()
                    image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))

            self.images[path] = image
            return image
        except pygame.error:
            print(f"Failed to load image: {name}")
            fallback = pygame.Surface((50, 50))
            fallback.fill((255, 0, 255))
            return fallback

    def get_sound(self, name: str) -> pygame.mixer.Sound | None:
        path = os.path.join(self.base_path, 'sounds', name)
        if path in self.sounds:
            return self.sounds[path]

        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[path] = sound
            return sound
        except pygame.error:
            print(f"Failed to load sound: {name}")
            return None

    def get_font(self, name: str, size: int) -> pygame.font.Font:
        path = os.path.join(self.base_path, 'fonts', name)
        key = (path, size)

        if key in self.fonts:
            return self.fonts[key]

        try:
            font = pygame.font.Font(path, size)
            self.fonts[key] = font
            return font
        except pygame.error:
            print(f"Failed to load font: {name}")
            return pygame.font.SysFont("Courier", size, bold=True)
