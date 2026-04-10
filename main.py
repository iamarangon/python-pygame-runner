# main.py
import pygame
import sys
from src.core.game import Game

def main() -> None:
    pygame.init()
    pygame.font.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass

    game = Game()
    try:
        game.run()
    except Exception as e:
        print(f"Game crashed: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
