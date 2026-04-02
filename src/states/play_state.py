# src/states/play_state.py
import pygame
from src.states.state import State
from src.entities.player import Player
from src.entities.background import Background
from src.core.spawner import Spawner
from src.core.settings import SCREEN_WIDTH, BASE_SCROLL_SPEED, MAX_SCROLL_SPEED, COLORS

class PlayState(State):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(self.game.config)
        self.background = Background()
        self.spawner = Spawner()
        
        diff_factor = self.game.config.get_difficulty_factor()
        self.base_speed = BASE_SCROLL_SPEED * diff_factor
        self.max_speed = MAX_SCROLL_SPEED * diff_factor
        self.scroll_speed = self.base_speed
        self.score = 0
        self.timer = 0 # in seconds to track phase
        self.phase = 1

    def enter_state(self):
        super().enter_state()

    def update(self, dt):
        self.timer += dt
        # Increase score proportionally using time
        self.score += 10 * dt 
        
        # Determine phase and progressive difficulty
        if self.timer < 30:
            self.phase = 1
            speed_ratio = self.timer / 30.0
            self.scroll_speed = self.base_speed + (self.max_speed - self.base_speed) * 0.3 * speed_ratio
        elif self.timer < 60:
            self.phase = 2
            speed_ratio = (self.timer - 30) / 30.0
            self.scroll_speed = self.base_speed + (self.max_speed - self.base_speed) * (0.3 + 0.4 * speed_ratio)
        else:
            self.phase = 3
            speed_ratio = min((self.timer - 60) / 60.0, 1.0)
            self.scroll_speed = self.base_speed + (self.max_speed - self.base_speed) * (0.7 + 0.3 * speed_ratio)

        # Update entities
        self.background.update(self.scroll_speed, dt)
        self.player.update(dt)
        self.spawner.update(self.phase, self.scroll_speed, dt)
        
        self.check_collisions()

    def check_collisions(self):
        for enemy in self.spawner.enemies:
            if self.player.rect.colliderect(enemy.rect):
                from src.states.game_over_state import GameOverState
                game_over_state = GameOverState(self.game, int(self.score), self.game.config.difficulty)
                game_over_state.enter_state()

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    from src.states.pause_state import PauseState
                    pause_state = PauseState(self.game)
                    pause_state.enter_state()

    def render(self, surface):
        self.background.render(surface)
        self.spawner.render(surface)
        self.player.render(surface)
        
        # Draw Score
        score_surf = self.game.font.render(f"Score: {int(self.score)}", True, COLORS["text_dark"])
        surface.blit(score_surf, (10, 10))
        
        # Draw Phase
        phase_surf = self.game.font.render(f"Phase: {self.phase}", True, COLORS["text_dark"])
        surface.blit(phase_surf, (SCREEN_WIDTH - 150, 10))
