import pygame
import sys
from src.core.game import Game

def main():
    pygame.init()
    pygame.font.init()
    
    # Check if a custom audio mixer initialization is needed, otherwise pygame.init() covers it.
    
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
