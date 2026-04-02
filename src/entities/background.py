# src/entities/background.py
import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, COLORS
from src.core.resource_loader import ResourceLoader

class Background:
    def __init__(self):
        rl = ResourceLoader()
        # Scale to match full screen dimensions
        self.sky_surf = rl.get_image("Sky.png", "images", scale=(SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Load ground image - needs wider loop setup for scrolling
        raw_ground = rl.get_image("ground.png", "images")
        
        # Ground assets from Clear Code are usually smaller so we tile them or stretch if needed
        # We will stretch it to match ground layer height and loop it horizontally
        ground_height = SCREEN_HEIGHT - GROUND_Y
        self.ground_surf = pygame.transform.scale(raw_ground, (SCREEN_WIDTH, ground_height))
        
        self.sky_color = COLORS["sky"] # Fallback
        self.sky_x1 = 0
        self.sky_x2 = SCREEN_WIDTH
        self.ground_x1 = 0
        self.ground_x2 = SCREEN_WIDTH
        
    def update_sky(self, scroll_speed, dt):
        self.sky_x1 -= scroll_speed * 0.5
        self.sky_x2 -= scroll_speed * 0.5
        
        if self.sky_x1 <= -SCREEN_WIDTH:
            self.sky_x1 = self.sky_x2 + SCREEN_WIDTH
        if self.sky_x2 <= -SCREEN_WIDTH:
            self.sky_x2 = self.sky_x1 + SCREEN_WIDTH
            
    def update_ground(self, scroll_speed, dt):
        self.ground_x1 -= int(scroll_speed)
        self.ground_x2 -= int(scroll_speed)
        
        if self.ground_x1 <= -SCREEN_WIDTH:
            self.ground_x1 = self.ground_x2 + SCREEN_WIDTH
        if self.ground_x2 <= -SCREEN_WIDTH:
            self.ground_x2 = self.ground_x1 + SCREEN_WIDTH
            
    def update(self, scroll_speed, dt):
        self.update_sky(scroll_speed, dt)
        self.update_ground(scroll_speed, dt)

    def render(self, surface):
        surface.blit(self.sky_surf, (self.sky_x1, 0))
        surface.blit(self.sky_surf, (self.sky_x2, 0))
        surface.blit(self.ground_surf, (self.ground_x1, GROUND_Y))
        surface.blit(self.ground_surf, (self.ground_x2, GROUND_Y))
