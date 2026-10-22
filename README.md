# RPS-AI

A small terminal rock-paper-scissors experiment. The AI starts with random moves, tracks your move history, then tries to counter your most frequent move.

## Run

```sh
uv run python main.py
```

Enter `r`, `p`, or `s` each round. Enter `q` to quit.

## Modules

- `rps.py` — moves and round rules.
- `ai.py` — adaptive opponent model and move selection.
- `cli.py` — terminal input and score display.
- `main.py` — connects the game loop.

This simple frequency-based strategy is an experiment, not a mind reader: random or changing moves can throw it off.
