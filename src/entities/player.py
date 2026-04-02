# src/entities/player.py
import pygame
from src.core.settings import SCREEN_HEIGHT, GROUND_Y, GRAVITY, JUMP_STRENGTH, FAST_FALL_STRENGTH, COLORS
from src.core.resource_loader import ResourceLoader

class Player:
    def __init__(self, config=None):
        rl = ResourceLoader()
        self.config = config
        
        # Load bases
        self.player_stand = rl.get_image("player_stand.png", "images/player")
        self.player_jump = rl.get_image("jump.png", "images/player")
        self.walk_frames = [
            rl.get_image("player_walk_1.png", "images/player"),
            rl.get_image("player_walk_2.png", "images/player")
        ]
        self.jump_sound = rl.get_sound("jump.mp3")
        
        # Setup Squashed walk frames for Ducking Mechanic
        # The user approved scaling Y by 50%
        self.duck_frames = []
        for frame in self.walk_frames:
            w, h = frame.get_size()
            duck_surf = pygame.transform.scale(frame, (w, int(h * 0.5)))
            self.duck_frames.append(duck_surf)
            
        self.frame_index = 0
        self.animation_speed = 10.0
        
        self.image = self.player_stand
        self.height_stand = self.player_stand.get_height()
        self.height_duck = int(self.height_stand * 0.5)
        
        # Position
        self.x = 100
        self.y = GROUND_Y - self.height_stand
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # Physics
        self.velocity_y = 0.0
        self.is_jumping = False
        self.is_ducking = False

    def handle_input(self, keys):
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not self.is_jumping and not self.is_ducking:
                self.velocity_y = JUMP_STRENGTH
                self.is_jumping = True
                if self.jump_sound:
                    vol = self.config.get_music_volume() if self.config else 0.5
                    self.jump_sound.set_volume(vol)
                    self.jump_sound.play()

        if keys[pygame.K_DOWN]:
            if not self.is_jumping:
                self.is_ducking = True
            else:
                self.velocity_y += FAST_FALL_STRENGTH
        else:
            self.is_ducking = False

    def update(self, dt):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += int(self.velocity_y)
        
        # Ground collision
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.velocity_y = 0
            self.is_jumping = False

        # Animation logic
        if self.is_jumping:
            self.image = self.player_jump
            # Adjust rect if we were ducking previously
            if self.rect.height != self.player_jump.get_height():
                self.rect = self.image.get_rect(bottomleft=(self.rect.x, self.rect.bottom))
        elif self.is_ducking:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.duck_frames):
                self.frame_index = 0
            self.image = self.duck_frames[int(self.frame_index)]
            # Stick to ground when ducking
            self.rect = self.image.get_rect(bottomleft=(self.rect.x, GROUND_Y))
        else:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0
            self.image = self.walk_frames[int(self.frame_index)]
            # Match standard height
            self.rect = self.image.get_rect(bottomleft=(self.rect.x, GROUND_Y))

    def render(self, surface):
        surface.blit(self.image, self.rect)
