# Architecture Design - Medieval Forest Runner

## Game Structure
The architecture follows an Object-Oriented Programming (OOP) approach focused on modularity and decoupling, according to the **MS-Framework AI** guidelines.

## Core Engine
- **GameLoop**: Manages the clock (`pygame.time.Clock`), events (`pygame.event`), and the central update/draw calls.
- **StateManager**: Manages transitions between screens (MENU, PLAYING, GAMEOVER).

## Entity System
All visible entities in the game inherit from a base class `GameEntity`.

### Animation States (Adventurer)
- `IDLE`: Standing still (main menu only).
- `RUNNING`: Moving horizontally.
- `JUMPING`: Starting the jump.
- `FALLING`: Descending from the jump.
- `CROUCHING`: Crouched/Sliding.
- `ATTACK_GROUND`: Attack on ground.
- `ATTACK_AIR`: Attack during air time.
- `ATTACK_CROUCH`: Attack while crouching.

## Combat System (Hitbox/Hurtbox)
For classic 2D combat, we use two types of rectangles:
1. **Hurtbox**: The entity's body. Detects if the entity was hit by an enemy or obstacle.
2. **Hitbox**: An area in front of the player during the attack animation. Detects if the attack hit an enemy.

## Parallax System (Depth)
- **Layer 0**: Sky (Static or very slow movement).
- **Layer 1**: Clouds (Slow movement).
- **Layer 2**: Distant Trees (Medium-slow movement).
- **Layer 3**: Close Trees (Medium movement).
- **Layer 4**: Ground (Grass + Earth, fast movement synced with the player).

## Data Flow
1. `InputHandler` captures pressed/released keys.
2. `PhysicsEngine` applies gravity and updates velocities.
3. `CollisionManager` checks collisions between Hitboxes, Hurtboxes, and the Ground.
4. `Renderer` draws sprites based on each entity's current state.

## Assets and Sprites
- **Format**: Spritesheets in **2D Classic (Side)** style.
- **Animations**: Frame-based (`frame_index`) incremented over time.
