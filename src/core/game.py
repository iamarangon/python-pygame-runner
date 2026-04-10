# src/core/game.py
import pygame
import os
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Game:
    def __init__(self) -> None:
        pygame.display.set_caption("Py-Runner")
        self.screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True

        from src.core.config import Config
        self.config = Config()

        from src.core.resource_loader import ResourceLoader
        self.rl = ResourceLoader()
        self.font = self.rl.get_font("Pixeltype.ttf", 36)
        self.menu_font = self.rl.get_font("Pixeltype.ttf", 46)
        self.title_font = self.rl.get_font("Pixeltype.ttf", 100)

        self.update_system_volume()

        music_path = os.path.join(self.rl.base_path, "sounds", "music.wav")
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

        self.state_stack: list = []

    def load_states(self) -> None:
        from src.states.menu_state import MenuState
        menu_state = MenuState(self)
        menu_state.enter_state()

    def update_system_volume(self) -> None:
        try:
            pygame.mixer.music.set_volume(self.config.get_music_volume())
        except pygame.error:
            pass

    def handle_events(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        if self.state_stack:
            self.state_stack[-1].handle_events(events)

    def update(self, dt: float) -> None:
        if self.state_stack:
            self.state_stack[-1].update(dt)

    def render(self) -> None:
        if self.state_stack:
            self.state_stack[-1].render(self.screen)
        pygame.display.flip()

    def run(self) -> None:
        self.load_states()
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()
