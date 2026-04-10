# src/states/pause_state.py
import pygame
from src.states.state import State
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, PAUSE_COUNTDOWN

class PauseState(State):
    def __init__(self, game):
        super().__init__(game)
        self.resume_timer = -1

    def enter_state(self):
        super().enter_state()

    def update(self, dt):
        if self.resume_timer > 0:
            self.resume_timer -= dt
            if self.resume_timer <= 0:
                self.exit_state()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.resume_timer == -1 and (event.key == pygame.K_SPACE or event.key == pygame.K_p):
                    self.resume_timer = PAUSE_COUNTDOWN

    def render(self, surface):
        if self.prev_state:
            self.prev_state.render(surface)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLORS["overlay"])
        surface.blit(overlay, (0, 0))

        center_x = SCREEN_WIDTH // 2

        if self.resume_timer > 0:
            count_str = str(int(self.resume_timer) + 1)
            count_surf = self.game.title_font.render(count_str, True, COLORS["white"])
            count_rect = count_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2))
            surface.blit(count_surf, count_rect)
        else:
            pause_surf = self.game.title_font.render("PAUSED", True, COLORS["white"])
            pause_rect = pause_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2))
            surface.blit(pause_surf, pause_rect)

            inst_surf = self.game.font.render("Press SPACE to Resume", True, COLORS["white"])
            inst_rect = inst_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 + 50))
            surface.blit(inst_surf, inst_rect)
