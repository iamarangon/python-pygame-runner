# src/states/options_state.py
import pygame
from src.states.state import State
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS

class OptionsState(State):
    def __init__(self, game):
        super().__init__(game)
        # Options row 
        # 0: Volume, 1: Difficulty, 2: Back
        self.selected_index = 0
        self.options = ["Volume", "Difficulty", "Back"]

    def enter_state(self):
        super().enter_state()

    def update(self, dt):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                
                # Handling Left/Right for Adjustments
                elif event.key == pygame.K_LEFT:
                    if self.selected_index == 0:  # Volume Drop
                        if self.game.config.volume > 0:
                            self.game.config.volume -= 1
                            self.game.update_system_volume()
                            self.game.config.save()
                    elif self.selected_index == 1: # Diff Drop
                        diffs = ["Easy", "Normal", "Hard"]
                        curr_idx = diffs.index(self.game.config.difficulty)
                        if curr_idx > 0:
                            self.game.config.difficulty = diffs[curr_idx - 1]
                            self.game.config.save()
                            
                elif event.key == pygame.K_RIGHT:
                    if self.selected_index == 0:  # Volume Increase
                        if self.game.config.volume < 4:
                            self.game.config.volume += 1
                            self.game.update_system_volume()
                            self.game.config.save()
                    elif self.selected_index == 1: # Diff Increase
                        diffs = ["Easy", "Normal", "Hard"]
                        curr_idx = diffs.index(self.game.config.difficulty)
                        if curr_idx < 2:
                            self.game.config.difficulty = diffs[curr_idx + 1]
                            self.game.config.save()
                            
                # Exiting State
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.selected_index == 2: # Back
                        self.exit_state()
                elif event.key == pygame.K_ESCAPE:
                    self.exit_state()

    def render(self, surface):
        surface.fill(COLORS["sky"])
        
        center_x = SCREEN_WIDTH // 2
        
        title_surf = self.game.title_font.render("OPTIONS", True, COLORS["text_dark"])
        title_rect = title_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 4))
        surface.blit(title_surf, title_rect)
        
        start_y = SCREEN_HEIGHT // 2
        
        for i, option in enumerate(self.options):
            color = COLORS["red"] if i == self.selected_index else COLORS["text"]
            
            # Format text based on type
            if option == "Volume":
                # Volume bar using pure text e.g. < |||| >
                vol_str = "|" * self.game.config.volume
                vol_str = vol_str.ljust(4, '.') # e.g. "||.."
                text = f"< Volume: [ {vol_str} ] >"
            elif option == "Difficulty":
                text = f"< Difficulty: {self.game.config.difficulty} >"
            else:
                text = option
            
            if i == self.selected_index:
                text = f"> {text} <" if option == "Back" else text
                
            opt_surf = self.game.font.render(text, True, color)
            opt_rect = opt_surf.get_rect(center=(center_x, start_y + (i * 40)))
            surface.blit(opt_surf, opt_rect)
        
        # Hint Instruction
        hint_surf = self.game.font.render("Use LEFT/RIGHT arrows to change values", True, COLORS["text_dark"])
        hint_rect = hint_surf.get_rect(center=(center_x, SCREEN_HEIGHT - 30))
        surface.blit(hint_surf, hint_rect)
