# src/states/leaderboard_state.py
import pygame
from src.states.state import State
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS

class LeaderboardState(State):
    def __init__(self, game):
        super().__init__(game)
        from src.core.scoreboard import ScoreBoard
        self.sb = ScoreBoard()
        self.scores = self.sb.get_scores()

    def enter_state(self):
        super().enter_state()

    def update(self, dt):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    self.exit_state() # Return to MenuState
                elif event.key == pygame.K_c:
                    self.sb.reset_scores()
                    self.scores = self.sb.get_scores()

    def render(self, surface):
        surface.fill(COLORS["sky"])
        
        center_x = SCREEN_WIDTH // 2
        
        # Title
        title_surf = self.game.title_font.render("TOP 10 LEADERBOARD", True, COLORS["text_dark"])
        title_rect = title_surf.get_rect(center=(center_x, 30))
        surface.blit(title_surf, title_rect)
        
        # Back and Clear hints
        hints_surf = self.game.font.render("SPACE/ESC to return | C to Clear", True, COLORS["text_dark"])
        hints_rect = hints_surf.get_rect(center=(center_x, SCREEN_HEIGHT - 20))
        surface.blit(hints_surf, hints_rect)
        
        # Get a smaller font for the 10 rows
        small_font = self.game.rl.get_font("Pixeltype.ttf", 26)
        hd_font = self.game.rl.get_font("Pixeltype.ttf", 36)
        
        difficulties = [
            ("Easy", SCREEN_WIDTH * 0.15),
            ("Normal", SCREEN_WIDTH * 0.5),
            ("Hard", SCREEN_WIDTH * 0.85)
        ]
        
        start_y = 80
        
        for diff_name, col_x in difficulties:
            # Column Header
            head_surf = hd_font.render(diff_name, True, COLORS["red"])
            head_rect = head_surf.get_rect(center=(col_x, start_y))
            surface.blit(head_surf, head_rect)
            
            # Scores for column
            col_scores = self.scores[diff_name]
            if not col_scores:
                empty_surf = small_font.render("---", True, COLORS["text_dark"])
                empty_rect = empty_surf.get_rect(center=(col_x, start_y + 30))
                surface.blit(empty_surf, empty_rect)
            else:
                for i, entry in enumerate(col_scores):
                    text = f"{i+1:2d}. {entry['name']} {entry['score']:>5d}"
                    entry_surf = small_font.render(text, True, COLORS["text_dark"])
                    # Use spacing of 22 pixels to fit 10 lines
                    entry_rect = entry_surf.get_rect(center=(col_x, start_y + 30 + (i * 24)))
                    surface.blit(entry_surf, entry_rect)
