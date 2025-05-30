# Cosmic Invader

This is a simple terminal-based shooter inspired by classic space invader games. 
The latest version adds color, stronger cosmic monsters and limited-use bombs to bring
more strategy into the action.

## How to Run

Run the game using Python 3 in a terminal that supports curses:

```bash
python -m cosmic_invader.game
```

Use the left and right arrow keys to move the ship. Press the spacebar to fire
regular shots. Press `b` to unleash a bomb that destroys aliens in your column
(you only have three). Cosmic monsters marked with `M` take two hits. Press `q`
to quit. Destroy all enemies before any reach your position to win the game.
