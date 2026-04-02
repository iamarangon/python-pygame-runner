import pytest
import pygame
from src.core.game import Game
from src.states.leaderboard_state import LeaderboardState
from src.states.game_over_state import GameOverState
from src.states.menu_state import MenuState


# ── LeaderboardState ────────────────────────────────────────────────────────

class TestLeaderboardState:
    def test_escape_exits(self):
        game = Game()
        lb = LeaderboardState(game)
        game.state_stack.append(lb)
        lb.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        assert lb not in game.state_stack

    def test_space_exits(self):
        game = Game()
        lb = LeaderboardState(game)
        game.state_stack.append(lb)
        lb.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)])
        assert lb not in game.state_stack

    def test_c_resets_scores(self):
        game = Game()
        lb = LeaderboardState(game)
        lb.sb.add_score("AAA", 999, "Normal")
        lb.scores = lb.sb.get_scores()
        assert len(lb.scores["Normal"]) > 0

        lb.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c)])
        assert len(lb.scores["Normal"]) == 0

    def test_enter_state(self):
        game = Game()
        lb = LeaderboardState(game)
        lb.enter_state()
        assert lb in game.state_stack

    def test_render_with_scores(self):
        """Render with entries to cover the populated scores branch."""
        game = Game()
        lb = LeaderboardState(game)
        lb.sb.add_score("AAA", 500, "Normal")
        lb.scores = lb.sb.get_scores()
        surface = pygame.Surface((800, 400))
        lb.render(surface)  # lines 64-66 (filled branch)

    def test_render_empty_scores(self):
        """Render with empty scores to cover the --- branch."""
        game = Game()
        lb = LeaderboardState(game)
        lb.sb.reset_scores()
        lb.scores = lb.sb.get_scores()
        surface = pygame.Surface((800, 400))
        lb.render(surface)  # lines 20-26 (empty branch)


# ── GameOverState ───────────────────────────────────────────────────────────

class TestGameOverState:
    def test_not_top_10_returns_to_menu(self):
        """When score is not top 10, SPACE clears stack and goes to menu."""
        game = Game()
        # Fill scoreboard with high scores so 0 is not top 10
        from src.core.scoreboard import ScoreBoard
        sb = ScoreBoard()
        for i in range(10):
            sb.add_score("ZZZ", 9999 - i, "Normal")

        go = GameOverState(game, 0, "Normal")
        assert go.is_top_10 is False
        game.state_stack.append(go)

        go.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)])
        # Stack should have been cleared and rebuilt with MenuState
        assert len(game.state_stack) == 1
        assert type(game.state_stack[0]).__name__ == "MenuState"

    def test_top_10_goes_to_naming(self):
        """When score IS top 10, SPACE goes to naming state."""
        game = Game()
        go = GameOverState(game, 99999, "Normal")
        assert go.is_top_10 is True
        game.state_stack.append(go)

        go.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)])
        # NamingState should now be top of stack
        assert type(game.state_stack[-1]).__name__ == "NamingState"

    def test_render_top_10_message(self):
        game = Game()
        go = GameOverState(game, 99999, "Normal")
        go.is_top_10 = True
        surface = pygame.Surface((800, 400))
        go.render(surface)

    def test_render_not_top_10_message(self):
        game = Game()
        go = GameOverState(game, 0, "Normal")
        go.is_top_10 = False
        surface = pygame.Surface((800, 400))
        go.render(surface)   # line 59


# ── MenuState ───────────────────────────────────────────────────────────────

class TestMenuState:
    def test_navigate_and_select_play(self):
        game = Game()
        menu = MenuState(game)
        game.state_stack.append(menu)
        menu.selected_index = 0  # Play
        menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
        # PlayState should have been pushed
        assert type(game.state_stack[-1]).__name__ == "PlayState"

    def test_navigate_and_select_options(self):
        game = Game()
        menu = MenuState(game)
        game.state_stack.append(menu)
        menu.selected_index = 1  # Options
        menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
        assert type(game.state_stack[-1]).__name__ == "OptionsState"

    def test_navigate_and_select_leaderboard(self):
        game = Game()
        menu = MenuState(game)
        game.state_stack.append(menu)
        menu.selected_index = 2  # Leaderboard
        menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
        assert type(game.state_stack[-1]).__name__ == "LeaderboardState"

    def test_navigate_and_select_exit(self):
        game = Game()
        menu = MenuState(game)
        game.state_stack.append(menu)
        menu.selected_index = 3  # Exit
        menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
        assert game.running is False

    def test_up_down_navigation(self):
        game = Game()
        menu = MenuState(game)
        menu.selected_index = 0
        menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)])
        assert menu.selected_index == 1
        menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)])
        assert menu.selected_index == 0
