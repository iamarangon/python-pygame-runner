import pygame
import sys
from src.state_manager import StateManager
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BLACK


class GameEngine:
    """
    Main entry point for the "Medieval Forest Runner" game.
    Handles the primary game loop, display initialization, and frame timing.
    """
    def __init__(self, width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT, title: str = "Medieval Forest Runner"):
        # Initialize Core Pygame
        pygame.init()
        
        # Display setup
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        
        # Timing
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.is_running = True
        
        # State Management
        self.state_manager = StateManager()

    def run(self):
        """Starts the main game loop: Event -> Update -> Drawing."""
        while self.is_running:
            # Calculate deltaTime (fraction of a second)
            dt = self.clock.tick(self.fps) / 1000.0
            
            # 1. Event Handling
            self.handle_events()
            
            # 2. Logic Update
            self.update(dt)
            
            # 3. Rendering
            self.draw()

    def handle_events(self):
        """Delegates event handling to the active state."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
        
        self.state_manager.handle_events(events)

    def update(self, dt: float):
        """Delegates logic update to the active state."""
        self.state_manager.update(dt)

    def draw(self):
        """Clears the screen and delegates drawing to the active state."""
        self.screen.fill(COLOR_BLACK)
        self.state_manager.draw(self.screen)
        pygame.display.flip()

    def quit(self):
        """Gracefully shuts down the engine."""
        pygame.quit()
        sys.exit()


def main():
    """Wrapper for console_scripts entry point."""
    engine = GameEngine()
    try:
        engine.run()
    finally:
        engine.quit()


if __name__ == "__main__":
    main()
