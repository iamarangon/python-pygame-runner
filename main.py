from src.engine import GameEngine
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


def main() -> None:
    """
    Project entry point. Initializes the GameEngine and starts 
    the main execution loop using settings from constants.py.
    """
    try:
        # Initialize and run the game engine
        # We can pass these explicitly or omit them to use constants.py defaults
        game = GameEngine(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            title="Medieval Forest Runner"
        )
        game.run()
    except Exception as error:
        print(f"An error occurred during game execution: {error}")
    finally:
        # Ensure resources are released if an exception occurs
        import pygame
        pygame.quit()


if __name__ == "__main__":
    main()
