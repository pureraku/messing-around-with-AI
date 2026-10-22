"""Data objects for paddles and the ball."""

from dataclasses import dataclass

from settings import BLUE, HEIGHT, PADDLE_HEIGHT, PADDLE_WIDTH, RED, WIDTH


@dataclass
class Paddle:
    x: float
    y: float
    color: object
    score: int = 0


@dataclass
class Ball:
    x: float = WIDTH / 2
    y: float = HEIGHT / 2
    vx: float = 0.0
    vy: float = 0.0


def create_paddles():
    y = (HEIGHT - PADDLE_HEIGHT) / 2
    return (
        Paddle(48, y, BLUE),
        Paddle(WIDTH - 48 - PADDLE_WIDTH, y, RED),
    )
