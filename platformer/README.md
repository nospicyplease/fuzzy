# Mario-Style Platformer

This folder contains a basic side-scrolling platformer built with Pygame.
You can start it from the repository root with `python run_platformer.py` or
by running `python -m platformer.main`.

## Asset Structure
Place your images in the `assets/` directory with the following filenames:

- `assets/player.png` – Player sprite
- `assets/enemy.png` – Enemy sprite
- `assets/ground.png` – Ground tile
- `assets/platform.png` – Platform tile
- `assets/flagpole.png` – Flag to complete the level

If any of these files are missing, the game will fall back to simple colored
rectangles so it still runs.
