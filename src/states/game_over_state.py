# src/states/game_over_state.py
import pygame
from src.states.state import State
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS

class GameOverState(State):
    def __init__(self, game, score, difficulty="Normal"):
        super().__init__(game)
        self.score = score
        self.difficulty = difficulty
        from src.core.scoreboard import ScoreBoard
        self.scoreboard = ScoreBoard()
        self.is_top_10 = self.scoreboard.is_top_10(score, self.difficulty)

    def enter_state(self):
        super().enter_state()

    def update(self, dt):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if self.is_top_10:
                        from src.states.naming_state import NamingState
                        naming_state = NamingState(self.game, self.score, self.difficulty)
                        
                        # Remove Game Over State and Play State from stack
                        self.game.state_stack.clear()
                        # Restore Menu State at bottom
                        from src.states.menu_state import MenuState
                        self.game.state_stack.append(MenuState(self.game))
                        
                        naming_state.enter_state()
                    else:
                        # Return to main menu
                        self.game.state_stack.clear()
                        from src.states.menu_state import MenuState
                        menu = MenuState(self.game)
                        menu.enter_state()

    def render(self, surface):
        surface.fill(COLORS["black"])
        
        center_x = SCREEN_WIDTH // 2
        
        title_surf = self.game.title_font.render("GAME OVER", True, COLORS["red"])
        title_rect = title_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 3))
        surface.blit(title_surf, title_rect)
        
        score_surf = self.game.font.render(f"Final Score: {self.score}", True, COLORS["white"])
        score_rect = score_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2))
        surface.blit(score_surf, score_rect)
        
        if self.is_top_10:
            msg_surf = self.game.font.render("NEW HIGH SCORE! Press SPACE", True, COLORS["green"])
        else:
            msg_surf = self.game.font.render("Press SPACE to return to Menu", True, COLORS["white"])
            
        msg_rect = msg_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 + 50))
        surface.blit(msg_surf, msg_rect)
