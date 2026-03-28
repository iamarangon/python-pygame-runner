import pygame
import random
from src.states.base_state import BaseState
from src.state_enums import GameState
from src.entities.player import Player
from src.entities.enemy import Slug, Fly
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_FOREST_BG, COLOR_GREY, 
    COLOR_WHITE, PLAYER_START_X, PLAYER_GROUND_Y,
    INITIAL_SPAWN_INTERVAL, MIN_SPAWN_INTERVAL,
    SPAWN_REDUCTION_SCORE_STEP, SPAWN_REDUCTION_AMOUNT,
    SCORE_TICK_RATE, FLY_HEIGHT_HEAD, FLY_HEIGHT_HIGH,
    PARALLAX_BASE_SPEED
)


class PlayState(BaseState):
    """
    Main gameplay screen. Orchestrates player movement, enemy spawning,
    collision detection, and simple scrolling background.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        
        # Player initialization
        self.player = Player(x=PLAYER_START_X, y=PLAYER_GROUND_Y)
        
        # Enemy management
        self.enemies = []
        self.spawn_timer = 0
        self.initial_spawn_interval = INITIAL_SPAWN_INTERVAL
        self.min_spawn_interval = MIN_SPAWN_INTERVAL
        
        # Scoring and progress
        self.score_accumulator = 0.0
        
        # Background System (Simplified)
        self.sky_surf = self.player.assets.get_image("Sky")
        self.sky_surf = pygame.transform.scale(self.sky_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.ground_surf = self.player.assets.get_image("ground")
        self.ground_width = self.ground_surf.get_width()
        self.ground_x = 0

    def on_enter(self) -> None:
        """Resets the game state when entering the Play scenario."""
        self.manager.session.current_score = 0
        self.score_accumulator = 0.0
        self.player = Player(x=PLAYER_START_X, y=PLAYER_GROUND_Y)
        self.enemies = []
        self.spawn_timer = 0
        self.ground_x = 0
        print("[PlayState] Game Session Reset.")

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Processes player input and pause commands."""
        self.player.handle_input()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_state(GameState.PAUSED)

    def update(self, dt: float) -> None:
        """Main game loop update for this state."""
        # Update Player
        self.player.update(dt)
        
        # Progress & Difficulty
        self._update_progression(dt)
        
        # Background scrolling (ground)
        # Scroll at the world speed
        self.ground_x -= PARALLAX_BASE_SPEED * dt
        if self.ground_x <= -self.ground_width:
            self.ground_x += self.ground_width
        
        # Handle Spawning
        self._handle_spawning(dt)
        
        # Difficulty Multiplier (Calculated based on score survival)
        # Used for enemy animation speed scaling
        anim_multiplier = 1.0 + (self.manager.session.current_score / 1000.0)
        
        # Update Enemies & Collision
        for enemy in self.enemies[:]:
            enemy.update(dt, animation_multiplier=anim_multiplier)
            
            # Check Collision
            if self.player.is_attacking and self.player.attack_rect.colliderect(enemy.rect):
                self.enemies.remove(enemy)
                self.score_accumulator += 50
                self.manager.session.current_score = int(self.score_accumulator)
                continue
            
            if self.player.rect.colliderect(enemy.rect):
                self._trigger_game_over()
                return
            
            if enemy.rect.right < 0:
                self.enemies.remove(enemy)

    def _update_progression(self, dt: float) -> None:
        """Increments score over time and scales difficulty."""
        self.score_accumulator += SCORE_TICK_RATE * dt
        self.manager.session.current_score = int(self.score_accumulator)

    def _handle_spawning(self, dt: float) -> None:
        """Spawns a new enemy based on current difficulty interval."""
        self.spawn_timer += dt
        score = self.manager.session.current_score
        current_interval = max(
            self.min_spawn_interval, 
            self.initial_spawn_interval - (score // SPAWN_REDUCTION_SCORE_STEP) * SPAWN_REDUCTION_AMOUNT
        )
        
        if self.spawn_timer >= current_interval:
            self._spawn_random_enemy()
            self.spawn_timer = 0

    def _spawn_random_enemy(self) -> None:
        """Creates either a Slug or a Fly at the right edge of the screen."""
        # Note: Slug is now Snail in assets but we use the class Slug
        enemy_type = random.choice(["slug", "fly"])
        spawn_x = self.screen_width + 100
        
        if enemy_type == "slug":
            new_enemy = Slug(x=spawn_x, y=528) 
        else:
            fly_y = random.choice([FLY_HEIGHT_HEAD, FLY_HEIGHT_HIGH])
            new_enemy = Fly(x=spawn_x, y=fly_y)
            
        self.enemies.append(new_enemy)

    def _trigger_game_over(self) -> None:
        """Finalizes the session and transitions to Game Over."""
        self.manager.change_state(GameState.GAME_OVER)

    def draw(self, screen: pygame.Surface) -> None:
        """Renders the game scene with Sky and scrolling Ground."""
        # 1. Background
        screen.blit(self.sky_surf, (0, 0))
        
        # 2. Scrolling Ground
        screen.blit(self.ground_surf, (self.ground_x, 560))
        # Fill gap
        if self.ground_x < 0:
            screen.blit(self.ground_surf, (self.ground_x + self.ground_width, 560))
        
        # 3. Entities
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
            
        # 4. HUD
        self._draw_hud(screen)

    def _draw_hud(self, screen: pygame.Surface) -> None:
        """Displays score information on screen."""
        assets = self.player.assets
        font = assets.get_font("Pixeltype", 28)
        score_surface = font.render(f"SCORE: {self.manager.session.current_score}", True, COLOR_WHITE)
        screen.blit(score_surface, (20, 20))
