# Py-Runner 🦅

A fast-paced, progressively scaling 2D endless runner built with **Python** and **Pygame-CE**. Run, jump, and slide through an infinite scrolling world while dodging terrestrial and aerial enemies. 

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)
![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5.7-green.svg)
![Tests](https://img.shields.io/badge/Pytest-Coverage%2097%25-brightgreen)

---

## 🎮 Gameplay Features

* **Progressive Difficulty:** The game is divided into three consecutive phases. As you survive longer, the global scrolling engine accelerates smoothly up to its max speed.
* **Physics & Momentum:** Control your character with customized gravity settings. You can leap out of danger, and use the *Fast-Fall* mechanic to aggressively slice through the air and immediately slide below incoming flying enemies.
* **Triple-Tier Scoring:** Integrated global difficulty selections (`Easy`, `Normal`, and `Hard`). High scores are routed directly into designated partitions out of a local `config.json` file.
* **Parallax Environment:** The main menu runs a separate detached cloud simulation, while the main game ties both the sky and the ground into an infinite, dual-layered parallax loop.
* **Persistent Audiovisual Options:** Fully navigable graphical menus allowing instant SFX and Global Track volume adjustments.

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/iamarangon/python-pygame-runner.git
   cd python-pygame-runner
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv .venv
   
   # Windows:
   .\.venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you use `pygame-ce` (Community Edition) instead of the standard `pygame` for massively improved runtime speeds and modern API support).*

4. **Launch the Game!**
   ```bash
   python main.py
   ```

---

## 🕹️ Controls

| Action | Key(s) |
| :--- | :--- |
| **Jump** | `UP Arrow` or `SPACE` |
| **Duck / Fast-Fall** | `DOWN Arrow` |
| **Navigate Menus** | `UP` / `DOWN` / `LEFT` / `RIGHT` |
| **Confirm Selection** | `ENTER` or `SPACE` |
| **Clear Leaderboard** | `C` (On the Leaderboard Screen) |
| **Pause Game** | `P` or `ESC` (During run) |

---

## 🧩 Architecture

Py-Runner utilizes a tightly coupled, object-oriented State Machine:
- **`src/core/game.py`**: The main game loop routing native `pygame.events` into the active State.
- **`src/states/`**: Controls UI isolation (Menu, Options, Play, Game Over, Leaderboard, Naming).
- **`src/core/resource_loader.py`**: A caching Singleton ensuring that PNGs, TTFs, and audio nodes are only loaded from the solid-state drive exactly once.
- **`tests/`**: Includes a fully decoupled headless logic suite using Pytest and Mocks to ensure rendering logic doesn't crash CI pipelines.

---

## 🚀 Next Steps (Refactoring Roadmap)

The next major sprint encompasses migrating the custom collision and positional looping system into the standard **ClearCode Architecture**:
1. Porting all Entities to inherit from native `pygame.sprite.Sprite`.
2. Encapsulating actors into `pygame.sprite.Group` and `pygame.sprite.GroupSingle` to leverage native engine culling and rapid `.draw()` buffers.
3. Transitioning the math-heavy `dt` spawner array loops into native `pygame.USEREVENT` triggers for frame-independent optimization. 

---

*Good luck chasing the High Score!*
<br>
**Created by Italo Marangon.**
