import pygame
import sys
from src.states.base_state import BaseState
from src.state_enums import GameState
from src.assets_manager import AssetManager
from src.persistence import save_high_score, load_high_scores
from src.constants import COLOR_GAMEOVER_BG, COLOR_WHITE, COLOR_GOLD, COLOR_DANGER_RED, COLOR_LIGHT_GREY


class GameOverState(BaseState):
    """
    Game Over screen. Displays final score and high score status.
    Provides options: 1 - Menu (Save as GUEST), 2 - Name Score, 3 - Exit.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.assets = AssetManager()
        self.font = self.assets.get_font("Pixeltype", 64)
        self.small_font = self.assets.get_font("Pixeltype", 32)
        
        self.title_text = self.font.render("GAME OVER", True, COLOR_DANGER_RED)
        
        # Options Text
        self.opt1_text = self.small_font.render("1. Return to Main Menu", True, COLOR_WHITE)
        self.opt2_text = self.small_font.render("2. Name Score (& Save)", True, COLOR_WHITE)
        self.opt3_text = self.small_font.render("3. EXIT Game", True, COLOR_WHITE)
        
        self.is_high_score = False
        self.score_text = None
        self.score = 0

    def on_enter(self) -> None:
        """Logic executed when transitioning to this state."""
        self.score = self.manager.session.current_score
        
        # Check if it would be a High Score (Top 10)
        high_scores = load_high_scores()
        self.is_high_score = len(high_scores) < 10 or any(self.score > hs['score'] for hs in high_scores)
        
        color = COLOR_GOLD if self.is_high_score else COLOR_WHITE
        prefix = "NEW HIGH SCORE!! " if self.is_high_score else "FINAL SCORE: "
        self.score_text = self.small_font.render(f"{prefix}{self.score}", True, color)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Processes choices 1, 2, or 3."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    save_high_score("GUEST", self.score)
                    self.manager.change_state(GameState.MENU)
                
                if event.key == pygame.K_2:
                    self.manager.change_state(GameState.NAMING)
                
                if event.key == pygame.K_3:
                    save_high_score("GUEST", self.score)
                    pygame.quit()
                    sys.exit()

    def update(self, dt: float) -> None:
        """Game Over update logic."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Renders the Game Over screen."""
        screen.fill(COLOR_GAMEOVER_BG)
        
        # Center components
        title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, 120))
        screen.blit(self.title_text, title_rect)
        
        if self.score_text:
            score_rect = self.score_text.get_rect(center=(screen.get_width() // 2, 220))
            screen.blit(self.score_text, score_rect)
            
        # Draw Options
        options_y = 350
        screen.blit(self.opt1_text, (screen.get_width() // 2 - 150, options_y))
        screen.blit(self.opt2_text, (screen.get_width() // 2 - 150, options_y + 40))
        screen.blit(self.opt3_text, (screen.get_width() // 2 - 150, options_y + 80))
