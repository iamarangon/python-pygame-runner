# src/states/menu_state.py
import pygame
from src.states.state import State
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, COLORS
from src.entities.background import Background
from src.core.resource_loader import ResourceLoader

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = ["Play", "Options", "Leaderboard", "Exit"]
        self.selected_index = 0
        
        self.background = Background()
        rl = ResourceLoader()
        self.player_image = rl.get_image("player_stand.png", "images/player")
        self.player_rect = self.player_image.get_rect(bottomleft=(100, GROUND_Y))

    def enter_state(self):
        super().enter_state()

    def update(self, dt):
        # The sky visually scrolls slowly
        self.background.update_sky(2.0, dt)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.selected_index == 0:
                        from src.states.play_state import PlayState
                        play_state = PlayState(self.game)
                        play_state.enter_state()
                    elif self.selected_index == 1:
                        from src.states.options_state import OptionsState
                        opts_state = OptionsState(self.game)
                        opts_state.enter_state()
                    elif self.selected_index == 2:
                        from src.states.leaderboard_state import LeaderboardState
                        lb_state = LeaderboardState(self.game)
                        lb_state.enter_state()
                    elif self.selected_index == 3:
                        self.game.running = False

    def render(self, surface):
        self.background.render(surface)
        surface.blit(self.player_image, self.player_rect)
        
        center_x = SCREEN_WIDTH // 2
        
        title_surf = self.game.title_font.render("PY-RUNNER", True, COLORS["yellow"])
        title_rect = title_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 4))
        surface.blit(title_surf, title_rect)
        
        # Controls mapping top right
        controls = ["UP/SPACE: Jump", "DOWN: Duck/Fast Fall"]
        for i, text in enumerate(controls):
            ctrl_surf = self.game.font.render(text, True, COLORS["text_dark"])
            ctrl_rect = ctrl_surf.get_rect(topright=(SCREEN_WIDTH - 10, 10 + (i * 20)))
            surface.blit(ctrl_surf, ctrl_rect)
        
        start_y = SCREEN_HEIGHT // 2
        for i, option in enumerate(self.options):
            color = COLORS["red"] if i == self.selected_index else COLORS["text_dark"]
            text = f"> {option} <" if i == self.selected_index else option
            
            opt_surf = self.game.menu_font.render(text, True, color)
            opt_rect = opt_surf.get_rect(center=(center_x, start_y + (i * 45)))
            surface.blit(opt_surf, opt_rect)
