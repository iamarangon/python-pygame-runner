# src/core/game.py
import pygame
import os
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.display.set_caption("Py-Runner")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Global Config
        from src.core.config import Config
        self.config = Config()
        
        # Font caching
        from src.core.resource_loader import ResourceLoader
        self.rl = ResourceLoader()
        self.font = self.rl.get_font("Pixeltype.ttf", 36)
        self.menu_font = self.rl.get_font("Pixeltype.ttf", 46)
        self.title_font = self.rl.get_font("Pixeltype.ttf", 100)
        
        # Load and play background music
        self.update_system_volume()
        
        bg_music_path = os.path.join(self.rl.base_path, 'sounds', 'music.wav')
        try:
            pygame.mixer.music.load(bg_music_path)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass # Ignoring if file is missing or headless mock tests

        # State Machine Stack
        self.state_stack = []
        
        # Load internal dependencies here later to avoid circular imports
        # self.load_states()

    def load_states(self):
        # We will import states here to avoid circular dependencies
        from src.states.menu_state import MenuState
        # Setup initial state
        self.menu_menu = MenuState(self)
        self.menu_menu.enter_state()

    def update_system_volume(self):
        try:
            pygame.mixer.music.set_volume(self.config.get_music_volume())
        except pygame.error:
            pass

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        # Pass events to the top state
        if self.state_stack:
            self.state_stack[-1].handle_events(events)

    def update(self, dt):
        if self.state_stack:
            self.state_stack[-1].update(dt)

    def render(self):
        if self.state_stack:
            self.state_stack[-1].render(self.screen)
        
        pygame.display.flip()

    def run(self):
        self.load_states()
        while self.running:
            # dt in seconds
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.render()
