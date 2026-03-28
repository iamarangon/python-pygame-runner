# Medieval Forest Runner

A snappy, retro-style infinite runner game built with **Pygame-CE**. Dodge slugs and flies in a mysterious medieval forest, save your high scores, and climb the global ranking.

## 🕹️ Controls

- **W / Arrow UP**: Jump
- **S / Arrow DOWN**: Crouch (dodges head-level flies)
- **SPACE / D / Arrow RIGHT**: Attack (Upcoming feature)
- **ESC**: Pause / Resume
- **Keyboard**: Direct text input for naming your score

## ✨ Features

- **Adaptive Difficulty**: The game speed and enemy spawn rate increase as your score grows.
- **Dynamic Entities**: Ground-based Slugs and altitude-varying Flies.
- **Persistent Ranking**: Top 10 High Score leaderboard saved locally in JSON.
- **State Management**: Robust scene transitions (Menu, Play, Pause, Naming, Game Over).
- **Asset Management**: Centralized resource loading with fallback systems.

## 🛠️ Requirements

- Python 3.10+
- Pygame-CE (`pip install pygame-ce`)

## 🚀 Getting Started

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## 🏗️ Project Structure

- `src/`: Source code modules.
  - `entities/`: Player and Enemy implementation.
  - `states/`: Game scenes (Menu, Play, etc.).
  - `constants.py`: Centralized configuration.
- `assets/`: Images and Fonts.
- `data/`: High score persistence.
- `tests/`: Automated unit tests.

---
**Author**: Italo Marangon
