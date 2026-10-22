# Blue vs Red AI Pong

A 2D automatic Pong match built with Python and Raylib. Blue and Red use different rule-based strategies; the `bot.py` module is the seam for future scikit-learn lessons.

## Run with uv

```sh
uv sync
uv run python main.py
```

The first paddle to 7 points wins. **Space** pauses/resumes, **R** restarts, and **Esc** quits.

## Modules

- `main.py` — window loop and input.
- `settings.py` — dimensions, colors, speed and randomness settings.
- `entities.py` — ball and paddle data.
- `bot.py` — Blue predicts a wall-reflected intercept; Red reacts to a delayed, noisy position.
- `game.py` — motion, randomized collisions, scoring and match state.
- `renderer.py` — Raylib drawing.

The ball serves faster than a standard Pong ball, speeds up after paddle contact, and receives small random changes at wall and paddle bounces. The current project only depends on Raylib; scikit-learn can be introduced when replacing either bot.
