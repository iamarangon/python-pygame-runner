# src/states/play_state.py
import pygame
from src.states.state import State
from src.entities.player import Player
from src.entities.background import Background
from src.core.spawner import Spawner
from src.core.settings import SCREEN_WIDTH, BASE_SCROLL_SPEED, MAX_SCROLL_SPEED, COLORS

class PlayState(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        
        self.player_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
        self.player_group.add(Player(self.game.config))
        
        self.obstacle_group: pygame.sprite.Group = pygame.sprite.Group()
        
        self.background = Background()
        self.spawner = Spawner()
        
        diff_factor: float = self.game.config.get_difficulty_factor()
        self.base_speed: float = BASE_SCROLL_SPEED * diff_factor
        self.max_speed: float = MAX_SCROLL_SPEED * diff_factor
        self.scroll_speed: float = self.base_speed
        
        self.score: float = 0.0
        self.timer: float = 0.0
        self.phase: int = 1
        
        self.spawn_event: int = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_event, self.spawner.get_dynamic_interval(self.phase))

    def enter_state(self) -> None:
        super().enter_state()

    def exit_state(self) -> None:
        pygame.time.set_timer(self.spawn_event, 0)
        super().exit_state()

    def update(self, dt: float) -> None:
        self.timer += dt
        self.score += 10 * dt 
        
        prev_phase = self.phase
        
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

        if self.phase != prev_phase:
            pygame.time.set_timer(self.spawn_event, self.spawner.get_dynamic_interval(self.phase))

        self.background.update(self.scroll_speed, dt)
        
        self.player_group.sprite.update(dt)

        for enemy in self.obstacle_group:
            enemy.update(self.scroll_speed, dt)
            if enemy.rect.right < 0:
                enemy.kill()

        self.check_collisions()

    def check_collisions(self) -> None:
        if pygame.sprite.spritecollide(self.player_group.sprite, self.obstacle_group, False):
            from src.states.game_over_state import GameOverState
            game_over_state = GameOverState(self.game, int(self.score), self.game.config.difficulty)
            game_over_state.enter_state()

    def handle_events(self, events) -> None:
        keys = pygame.key.get_pressed()
        self.player_group.sprite.handle_input(keys)
        
        for event in events:
            if event.type == self.spawn_event:
                self.spawner.spawn(self.phase, self.obstacle_group)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    from src.states.pause_state import PauseState
                    pause_state = PauseState(self.game)
                    pause_state.enter_state()

    def render(self, surface: pygame.Surface) -> None:
        self.background.render(surface)
        
        self.obstacle_group.draw(surface)
        self.player_group.draw(surface)
        
        score_surf = self.game.font.render(f"Score: {int(self.score)}", True, COLORS["text_dark"])
        surface.blit(score_surf, (10, 10))
        
        phase_surf = self.game.font.render(f"Phase: {self.phase}", True, COLORS["text_dark"])
        surface.blit(phase_surf, (SCREEN_WIDTH - 150, 10))
