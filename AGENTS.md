# AGENTS.md - Development Guidelines for Cosmic Invaders

## Build/Run Commands
- **Run game**: `python3 main.py`
- **Syntax check**: `python3 -m py_compile main.py`
- **Install dependencies**: `pip install pygame` (only pygame required)
- **No tests**: This project has no test suite currently

## Code Style & Conventions
- **Language**: Python 3.x with pygame library
- **File structure**: Single-file game in `main.py`
- **Imports**: Standard library first, then pygame, use `os.path.join` for file paths
- **Constants**: ALL_CAPS for global constants (WIDTH, HEIGHT, images, sounds)
- **Classes**: PascalCase (Ship, Player, Enemy, Laser, Explosion, MysteryEnemy)
- **Variables**: snake_case (enemy_vel, laser_vel, wave_length)
- **Assets**: Use relative paths with `os.path.join("folder", "file")`

## Code Patterns
- **Classes inherit from Ship**: Player, Enemy, MysteryEnemy extend base Ship class
- **Global variables**: Used for score, explosions, mystery_enemy (consider refactoring)
- **Asset loading**: Load all images/sounds at module level as constants
- **Game loop**: Standard pygame event loop with clock.tick(FPS)
- **Collision detection**: Uses pygame.mask for pixel-perfect collision

## Known Issues
- **Syntax Error**: Line 9 missing semicolon between pygame.mixer.init() and pygame.font.init()
- **Global state**: Heavy use of global variables makes code harder to maintain