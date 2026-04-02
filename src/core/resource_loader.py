# src/core/resource_loader.py
import pygame
import os

class ResourceLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceLoader, cls).__new__(cls)
            cls._instance.images = {}
            cls._instance.sounds = {}
            cls._instance.fonts = {}
            cls._instance.base_path = os.path.join(os.getcwd(), 'assets')
        return cls._instance

    def get_image(self, name, subfolder="images", scale=None):
        path = os.path.join(self.base_path, subfolder, name)
        
        # Check cache
        if path in self.images:
            return self.images[path]
            
        try:
            image = pygame.image.load(path)
            # Safely optimize image formatting dynamically
            if pygame.display.get_surface():
                image = image.convert_alpha()
            
            if scale:
                # scale receives a tuple (width, height) OR a multiplier (float)
                if isinstance(scale, tuple):
                    image = pygame.transform.scale(image, scale)
                elif isinstance(scale, (float, int)):
                    size = image.get_size()
                    image = pygame.transform.scale(image, (int(size[0]*scale), int(size[1]*scale)))
            
            self.images[path] = image
            return image
        except pygame.error as e:
            print(f"Failed to load image: {path} - {e}")
            # Return a fallback pink surface
            fallback = pygame.Surface((50, 50))
            fallback.fill((255, 0, 255))
            return fallback

    def get_sound(self, name):
        path = os.path.join(self.base_path, 'sounds', name)
        if path in self.sounds:
            return self.sounds[path]
            
        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[path] = sound
            return sound
        except pygame.error as e:
            print(f"Failed to load sound: {path} - {e}")
            return None

    def get_font(self, name, size):
        path = os.path.join(self.base_path, 'fonts', name)
        # Font cache key combines path and size
        key = (path, size)
        
        if key in self.fonts:
            return self.fonts[key]
            
        try:
            font = pygame.font.Font(path, size)
            self.fonts[key] = font
            return font
        except pygame.error as e:
            print(f"Failed to load font: {path} - {e}")
            return pygame.font.SysFont("Courier", size, bold=True)
