# Py-Runner 🦅

A fast-paced, progressively scaling 2D endless runner built with **Python** and **Pygame-CE**.
Run, jump, and duck through an infinite scrolling world while dodging ground and aerial enemies.

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)
![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5.7-green.svg)
![Tests](https://img.shields.io/badge/Tests-80%20passing%20%7C%2096%25%20coverage-brightgreen)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black)

---

## 🎮 Gameplay

- **3 Phases of Progressive Difficulty:** Scroll speed ramps smoothly across three timed phases. Survive long enough and the world becomes relentless.
- **Physics & Momentum:** Jump, Fast-Fall mid-air, or duck under aerial enemies. Gravity is tuned for responsive, satisfying control.
- **Triple-Tier Leaderboard:** Scores are tracked separately per difficulty (`Easy`, `Normal`, `Hard`) and persist between sessions via a local `data/scores.json`.
- **Persistent Settings:** Volume and difficulty are saved automatically between sessions via `data/config.json`.
- **Parallax Environment:** Dual-layer infinite scrolling sky and ground, with a separate cloud simulation in the main menu.

---

## 🚀 Download & Play

> Download the latest pre-built executable for your platform from the [**Releases**](../../releases) page — no Python required.

| Platform | File |
|----------|------|
| Windows  | `py-runner-windows.exe` |
| Linux    | `py-runner-linux` |
| macOS    | `py-runner-macos` |

---

## 🛠️ Run from Source

1. **Clone:**
   ```bash
   git clone https://github.com/iamarangon/python-pygame-runner.git
   cd python-pygame-runner
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv

   # Windows:
   .\.venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install runtime dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Play:**
   ```bash
   python main.py
   ```

---

## 🕹️ Controls

| Action | Key(s) |
| :--- | :--- |
| **Jump** | `SPACE` or `↑` |
| **Duck / Fast-Fall** | `↓` |
| **Navigate Menus** | `↑` / `↓` / `←` / `→` |
| **Confirm** | `ENTER` or `SPACE` |
| **Pause** | `P` or `ESC` |
| **Clear Leaderboard** | `C` (Leaderboard screen) |

---

## 🧩 Architecture

| Layer | Description |
|-------|-------------|
| `main.py` | Entry point — initializes Pygame and starts the Game loop |
| `src/core/game.py` | Central game loop — routes events into the active State |
| `src/states/` | State machine: Menu, Play, Pause, Game Over, Leaderboard, Options, Naming |
| `src/entities/` | Sprite-based entities: `Player`, `Enemy`, `Background` |
| `src/core/spawner.py` | Injects enemy sprites into Groups via `pygame.USEREVENT` timers |
| `src/core/resource_loader.py` | Singleton asset cache — loads each image, sound, and font once |
| `src/core/settings.py` | Central constants: screen, physics, difficulty, timing |
| `tests/` | 80 headless tests, 96% coverage — fully compatible with CI (no display or audio device required) |

---

## 🧪 Run Tests

```bash
pip install -r requirements-dev.txt
pytest --cov=src tests/
```

---

## 🙌 Credits & Attributions

The initial code structure was developed following the excellent tutorial by the **Clear Code** YouTube channel. 
- **YouTube Channel:** [Clear Code](https://www.youtube.com/@ClearCode)
- **Tutorial Link:** [The ultimate introduction to Pygame](https://www.youtube.com/watch?v=AY9MnQ4x3zk&list=PLsIbpk0M-XAlhSR7Bc6B7ef5h_PWkNA2B&index=1&t=2319s)

All visual sprites and assets used in this project are kindly provided by his repository.
- **Project Repository:** [UltimatePygameIntro](https://github.com/clear-code-projects/UltimatePygameIntro)
- **Clear Code GitHub Profile:** [clear-code-projects](https://github.com/clear-code-projects)

---

*Good luck chasing the High Score!*
<br>
**Refactored & Expanded by Italo Marangon.**
