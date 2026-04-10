"""
Tests for the build entrypoint — validates that main.py is importable and
that all assets referenced at startup exist. Runs headless (no display needed).
These tests serve as the CI gate before PyInstaller packages the executable.
"""
import importlib
import os
import sys
import pytest


ASSET_DIRS = [
    "assets/images",
    "assets/images/player",
    "assets/images/snail",
    "assets/images/fly",
    "assets/fonts",
    "assets/sounds",
]

REQUIRED_ASSETS = [
    "assets/fonts/Pixeltype.ttf",
    "assets/images/Sky.png",
    "assets/images/ground.png",
    "assets/images/player/player_stand.png",
    "assets/images/player/player_walk_1.png",
    "assets/images/player/player_walk_2.png",
    "assets/images/player/jump.png",
    "assets/images/snail/snail1.png",
    "assets/images/snail/snail2.png",
    "assets/images/fly/fly1.png",
    "assets/images/fly/fly2.png",
]


class TestBuildRequirements:
    def test_main_module_importable(self):
        """main.py must be importable without launching the game window."""
        spec = importlib.util.spec_from_file_location("main", "main.py")
        assert spec is not None, "main.py could not be located"
        module = importlib.util.module_from_spec(spec)
        assert module is not None

    def test_src_package_structure(self):
        """All src sub-packages must be importable."""
        packages = [
            "src.core.game",
            "src.core.config",
            "src.core.settings",
            "src.core.scoreboard",
            "src.core.spawner",
            "src.core.resource_loader",
            "src.entities.player",
            "src.entities.enemies",
            "src.entities.background",
            "src.states.state",
            "src.states.menu_state",
            "src.states.play_state",
            "src.states.pause_state",
            "src.states.game_over_state",
            "src.states.naming_state",
            "src.states.options_state",
            "src.states.leaderboard_state",
        ]
        for pkg in packages:
            assert importlib.util.find_spec(pkg) is not None, f"Package not found: {pkg}"

    def test_required_asset_dirs_exist(self):
        """All asset directories that PyInstaller will bundle must exist."""
        for directory in ASSET_DIRS:
            assert os.path.isdir(directory), f"Missing asset directory: {directory}"

    def test_required_asset_files_exist(self):
        """All critical asset files must exist before packaging."""
        missing = [f for f in REQUIRED_ASSETS if not os.path.isfile(f)]
        assert not missing, f"Missing asset files:\n" + "\n".join(f"  - {f}" for f in missing)

    def test_data_dir_gitignored(self):
        """data/ must be in .gitignore — scores and config must NOT be bundled."""
        with open(".gitignore", "r") as f:
            content = f.read()
        assert "data/" in content, "data/ must be listed in .gitignore to prevent bundling user saves"

    def test_spec_file_exists(self):
        """PyInstaller spec file must exist for the release workflow."""
        assert os.path.isfile("py-runner.spec"), "py-runner.spec is required for PyInstaller packaging"

    def test_requirements_split(self):
        """requirements-dev.txt must exist and reference requirements.txt."""
        assert os.path.isfile("requirements-dev.txt"), "requirements-dev.txt is required for CI"
        with open("requirements-dev.txt", "r") as f:
            content = f.read()
        assert "-r requirements.txt" in content, "requirements-dev.txt must include -r requirements.txt"

    def test_pyinstaller_in_dev_requirements(self):
        """pyinstaller must be declared in requirements-dev.txt."""
        with open("requirements-dev.txt", "r") as f:
            content = f.read().lower()
        assert "pyinstaller" in content, "pyinstaller must be listed in requirements-dev.txt"
