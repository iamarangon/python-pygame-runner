import pygame
from src.assets_manager import AssetManager
from src.entities.base_entity import GameEntity
from src.constants import (
    PLAYER_SIZE, PLAYER_CROUCH_HEIGHT, PLAYER_GRAVITY, 
    PLAYER_JUMP_VELOCITY, PLAYER_GROUND_Y, COLOR_UI_PLAYER
)


class Player(GameEntity):
    """
    Adventurer player with rigid, snappy physics and multiple animation states:
    STAND, WALK, JUMP.
    """
    def __init__(self, x: float, y: float):
        self.original_height = PLAYER_SIZE[1]
        self.crouch_height = PLAYER_CROUCH_HEIGHT
        
        # Initialize
        super().__init__(x, y, PLAYER_SIZE[0], self.original_height, color=COLOR_UI_PLAYER)
        
        self.assets = AssetManager()
        
        # Load and scale Animation Frames from subfolders
        self.stand_surf = pygame.transform.scale(self.assets.get_image("player/player_stand"), PLAYER_SIZE)
        self.jump_surf = pygame.transform.scale(self.assets.get_image("player/jump"), PLAYER_SIZE)
        self.walk_frames = [
            pygame.transform.scale(self.assets.get_image("player/player_walk_1"), PLAYER_SIZE),
            pygame.transform.scale(self.assets.get_image("player/player_walk_2"), PLAYER_SIZE)
        ]
        
        # Animation State
        self.animation_index = 0.0
        self.animation_speed = 10.0 # Frames per second
        self.sprite = self.stand_surf # Starting sprite
        
        # Physics
        self._gravity = PLAYER_GRAVITY
        self._jump_velocity = PLAYER_JUMP_VELOCITY
        self._ground_y = y
        self.is_on_ground = True
        self.is_crouching = False
        
        # Attack Logic
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 0.3
        self.attack_cooldown = 0.5
        self.can_attack = True
        self.cooldown_timer = 0
        # Hitbox for attack (in front of the player)
        # Increased size and adjusted position
        self.attack_rect = pygame.Rect(0, 0, 80, 50)

    def handle_input(self) -> None:
        """Captures jump, crouch, and action commands."""
        keys = pygame.key.get_pressed()
        
        # Jump command
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.is_on_ground and not self.is_crouching:
            self.velocity.y = self._jump_velocity
            self.is_on_ground = False

        # Crouch command
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.is_on_ground:
            self._start_crouch()
        elif self.is_crouching:
            self._stop_crouch()
            
        # Attack command
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.can_attack and not self.is_attacking:
            self._start_attack()

    def _start_crouch(self):
        if not self.is_crouching:
            self.is_crouching = True
            self.rect.height = self.crouch_height
            self.rect.y = self._ground_y + (self.original_height - self.crouch_height)

    def _stop_crouch(self):
        self.is_crouching = False
        self.rect.height = self.original_height
        self.rect.y = self._ground_y

    def _start_attack(self):
        self.is_attacking = True
        self.can_attack = False
        self.attack_timer = self.attack_duration
        self.cooldown_timer = self.attack_cooldown

    def update(self, dt: float) -> None:
        """Applies physics and updates animation frames."""
        # Physics update
        self.apply_gravity(self._gravity, dt)
        self.rect.y += self.velocity.y * dt
        
        if self.rect.bottom >= self._ground_y + self.original_height:
            self.rect.bottom = self._ground_y + self.original_height
            self.velocity.y = 0
            self.is_on_ground = True
            
        # Timers
        if self.is_attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0: self.is_attacking = False
        if not self.can_attack:
            self.cooldown_timer -= dt
            if self.cooldown_timer <= 0: self.can_attack = True
                
        # Update Attack Rect position (Relative to player)
        # Shifted down slightly to avoid "eye-level" attack
        self.attack_rect.midleft = (self.rect.right, self.rect.centery + 10)
        
        # Animation selection
        self._animate(dt)

    def _animate(self, dt: float):
        """Updates the active sprite based on current state."""
        if not self.is_on_ground:
            # Jumping
            self.sprite = self.jump_surf
        elif self.is_crouching:
            # Crouching (using stand surf scaled down to crouch height)
            self.sprite = pygame.transform.scale(self.stand_surf, (PLAYER_SIZE[0], self.crouch_height))
        else:
            # Running
            self.animation_index += self.animation_speed * dt
            if self.animation_index >= len(self.walk_frames):
                self.animation_index = 0
            self.sprite = self.walk_frames[int(self.animation_index)]

    def draw(self, screen: pygame.Surface) -> None:
        """Renders the animated sprite."""
        # Center the sprite in the rect if needed, but here they should match
        screen.blit(self.sprite, self.rect)
        
        if self.is_attacking:
            pygame.draw.line(screen, (255, 255, 255), self.rect.midright, (self.rect.right + 30, self.rect.centery), 4)
