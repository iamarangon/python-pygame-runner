import pygame
import sys
from src.states.base_state import BaseState
from src.assets_manager import AssetManager
from src.state_enums import GameState
from src.persistence import load_high_scores
from src.constants import COLOR_MENU_BG, COLOR_WHITE, COLOR_GOLD, COLOR_SILVER, COLOR_BRONZE, COLOR_LIGHT_GREY


class MenuState(BaseState):
    """
    Main menu screen. Handles theme visualization, ranking display,
    and starting the game session.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.assets = AssetManager()
        
        # Load fonts via AssetManager
        self.font = self.assets.get_font("Pixeltype", 48)
        self.small_font = self.assets.get_font("Pixeltype", 24)
        self.tiny_font = self.assets.get_font("Pixeltype", 18)
        
        # Pre-render static text
        self.title_text = self.font.render("Medieval Forest Runner", True, (255, 255, 255))
        self.start_text = self.small_font.render("Press ENTER to Start", True, (200, 200, 200))
        self.ranking_title = self.small_font.render("TOP 10 RANKINGS", True, (255, 215, 0))
        
        # High score data
        self.high_scores = []
        self.ranking_surfaces = []

    def on_enter(self) -> None:
        """Logic executed when transitioning to this state (refresh ranking)."""
        self.high_scores = load_high_scores()
        self.ranking_surfaces = []
        
        for i, entry in enumerate(self.high_scores):
            score_str = f"{i+1}. {entry['name']}: {entry['score']}"
            color = (255, 255, 255)
            # Highlight Top 3
            if i == 0: color = (255, 215, 0) # Gold
            elif i == 1: color = (192, 192, 192) # Silver
            elif i == 2: color = (205, 127, 50) # Bronze
            
            surface = self.tiny_font.render(score_str, True, color)
            self.ranking_surfaces.append(surface)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Processes ENTER key to transition to the PLAYING state."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.manager.change_state(GameState.PLAYING)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def update(self, dt: float) -> None:
        """Menu state update logic."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Renders the menu screen with the Top 10 rankings."""
        screen.fill(COLOR_MENU_BG)
        
        # Title & Start
        title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, 80))
        screen.blit(self.title_text, title_rect)
        
        start_rect = self.start_text.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(self.start_text, start_rect)
        
        # Rankings Box (Right side)
        ranking_x = screen.get_width() // 2 + 50
        ranking_y = 220
        screen.blit(self.ranking_title, (ranking_x, ranking_y))
        
        for i, surface in enumerate(self.ranking_surfaces):
            screen.blit(surface, (ranking_x, ranking_y + 40 + i * 25))
            
        # Draw a simple "Runner" placeholder for visual balance
        player_preview = pygame.Surface((64, 64))
        player_preview.fill((0, 128, 255))
        screen.blit(player_preview, (screen.get_width() // 4, 300))
