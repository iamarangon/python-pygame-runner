# src/entities/player.py
import pygame
from src.core.settings import GROUND_Y, GRAVITY, JUMP_STRENGTH, FAST_FALL_STRENGTH
from src.core.resource_loader import ResourceLoader

DUCK_SCALE: float = 0.5

class Player(pygame.sprite.Sprite):
    def __init__(self, config=None) -> None:
        super().__init__()
        rl = ResourceLoader()
        self.config = config

        self.player_stand = rl.get_image("player_stand.png", "images/player")
        self.player_jump = rl.get_image("jump.png", "images/player")
        self.walk_frames: list[pygame.Surface] = [
            rl.get_image("player_walk_1.png", "images/player"),
            rl.get_image("player_walk_2.png", "images/player"),
        ]
        self.jump_sound = rl.get_sound("jump.mp3")

        self.duck_frames: list[pygame.Surface] = [
            pygame.transform.scale(f, (f.get_width(), int(f.get_height() * DUCK_SCALE)))
            for f in self.walk_frames
        ]

        self.frame_index: float = 0.0
        self.animation_speed: float = 10.0

        self.image: pygame.Surface = self.player_stand
        self.height_stand: int = self.player_stand.get_height()

        self.x: int = 100
        self.y: int = GROUND_Y - self.height_stand
        self.rect: pygame.Rect = self.image.get_rect(topleft=(self.x, self.y))

        self.velocity_y: float = 0.0
        self.is_jumping: bool = False
        self.is_ducking: bool = False

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
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

    def update(self, dt: float) -> None:
        self.velocity_y += GRAVITY
        self.rect.y += int(self.velocity_y)

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.velocity_y = 0
            self.is_jumping = False

        if self.is_jumping:
            self.image = self.player_jump
            if self.rect.height != self.player_jump.get_height():
                self.rect = self.image.get_rect(bottomleft=(self.rect.x, self.rect.bottom))
        elif self.is_ducking:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.duck_frames):
                self.frame_index = 0
            self.image = self.duck_frames[int(self.frame_index)]
            self.rect = self.image.get_rect(bottomleft=(self.rect.x, GROUND_Y))
        else:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0
            self.image = self.walk_frames[int(self.frame_index)]
            self.rect = self.image.get_rect(bottomleft=(self.rect.x, GROUND_Y))

