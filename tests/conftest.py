import pytest
import pygame
from src.assets_manager import AssetManager

@pytest.fixture(autouse=True)
def reset_asset_manager():
    """Resets the AssetManager singleton before each test to ensure isolation."""
    AssetManager._instance = None
    yield
