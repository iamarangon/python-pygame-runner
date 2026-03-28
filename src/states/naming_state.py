import pygame
from src.states.base_state import BaseState
from src.state_enums import GameState
from src.assets_manager import AssetManager
from src.persistence import save_high_score
from src.constants import COLOR_NAMING_BG, COLOR_WHITE, COLOR_GOLD, COLOR_LIGHT_GREY, MAX_NAME_LENGTH


class NamingState(BaseState):
    """
    State for entering the player's name via physical keyboard.
    Limited by MAX_NAME_LENGTH characters. Saves to persistence on ENTER.
    """
    def __init__(self, manager):
        super().__init__(manager)
        self.assets = AssetManager()
        self.font = self.assets.get_font("Pixeltype", 64)
        self.small_font = self.assets.get_font("Pixeltype", 32)
        
        self.title_text = self.font.render("ENTER YOUR NAME", True, COLOR_GOLD)
        self.instruction_text = self.small_font.render("Press ENTER to Save Score", True, COLOR_LIGHT_GREY)
        
        self.player_name = ""
        self.max_chars = MAX_NAME_LENGTH

    def on_enter(self) -> None:
        """Starts capturing text input."""
        pygame.key.start_text_input()
        self.player_name = ""

    def on_exit(self) -> None:
        """Stops capturing text input."""
        pygame.key.stop_text_input()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Processes physical keyboard typing and control keys."""
        for event in events:
            if event.type == pygame.TEXTINPUT:
                if len(self.player_name) < self.max_chars:
                    self.player_name += event.text
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                
                if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                    # Save the score with the new name
                    save_high_score(self.player_name, self.manager.session.current_score)
                    self.manager.session.is_new_high_score = False # Reset flag
                    self.on_exit()
                    self.manager.change_state(GameState.MENU)
                
                if event.key == pygame.K_ESCAPE:
                    self.on_exit()
                    self.manager.change_state(GameState.GAME_OVER)

    def update(self, dt: float) -> None:
        """Update logic (idle)."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Renders the text input screen."""
        screen.fill(COLOR_NAMING_BG)
        
        # Title
        title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, 180))
        screen.blit(self.title_text, title_rect)
        
        # Current Name Input
        name_surface = self.font.render(self.player_name + "_", True, COLOR_WHITE)
        name_rect = name_surface.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(name_surface, name_rect)
        
        # Instruction
        inst_rect = self.instruction_text.get_rect(center=(screen.get_width() // 2, 450))
        screen.blit(self.instruction_text, inst_rect)
