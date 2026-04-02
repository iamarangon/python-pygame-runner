# src/states/naming_state.py
import pygame
from src.states.state import State
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS

class NamingState(State):
    def __init__(self, game, score, difficulty="Normal"):
        super().__init__(game)
        self.score = score
        self.difficulty = difficulty
        self.name = ""

    def enter_state(self):
        super().enter_state()

    def update(self, dt):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Save Score and exit
                    if self.name.strip() == "":
                        self.name = "AAA"
                    from src.core.scoreboard import ScoreBoard
                    sb = ScoreBoard()
                    sb.add_score(self.name.strip().upper(), self.score, self.difficulty)
                    self.exit_state() # return to menu
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    if len(self.name) < 3 and event.unicode.isalpha():
                        self.name += event.unicode.upper()

    def render(self, surface):
        surface.fill(COLORS["sky"])
        
        center_x = SCREEN_WIDTH // 2
        
        title_surf = self.game.title_font.render("NEW HIGH SCORE", True, COLORS["text_dark"])
        title_rect = title_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 4))
        surface.blit(title_surf, title_rect)
        
        inst_surf = self.game.font.render("Type 3 Initials and press ENTER", True, COLORS["text_dark"])
        inst_rect = inst_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 - 30))
        surface.blit(inst_surf, inst_rect)
        
        # Draw input box
        box_width = 150
        box_rect = pygame.Rect(center_x - box_width//2, SCREEN_HEIGHT // 2 + 20, box_width, 60)
        pygame.draw.rect(surface, COLORS["white"], box_rect)
        pygame.draw.rect(surface, COLORS["black"], box_rect, 3)
        
        name_surf = self.game.title_font.render(self.name, True, COLORS["text_dark"])
        name_rect = name_surf.get_rect(center=box_rect.center)
        surface.blit(name_surf, name_rect)
