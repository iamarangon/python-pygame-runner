import pygame
from src.states.base_state import BaseState
from src.state_enums import GameState
from src.assets_manager import AssetManager
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_BLACK, PAUSE_OVERLAY_ALPHA


class PauseState(BaseState):
    """
    Pause overlay screen. Semi-transparent black background.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.assets = AssetManager()
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.set_alpha(PAUSE_OVERLAY_ALPHA)
        self.overlay.fill(COLOR_BLACK)
        
        # Load font directly
        self.font = self.assets.get_font("Pixeltype", 64)
        self.pause_text = self.font.render("PAUSED", True, COLOR_WHITE)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Processes ESC to resume."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    self.manager.change_state(GameState.PLAYING)

    def update(self, dt: float) -> None:
        """Pause logic (frozen)."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Renders the pause overlay on top of the current frame."""
        # Draw the current PlayState behind the overlay
        self.manager._states[GameState.PLAYING].draw(screen)
        
        # Apply overlay
        screen.blit(self.overlay, (0, 0))
        
        # Draw Text
        text_rect = self.pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(self.pause_text, text_rect)
