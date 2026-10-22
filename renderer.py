"""Raylib drawing routines."""

import pyray as rl

from settings import (
    BACKGROUND, BALL_RADIUS, BLUE, HEIGHT, MUTED, PADDLE_HEIGHT,
    PADDLE_WIDTH, RED, WHITE, WIDTH,
)


def draw(game):
    rl.begin_drawing()
    rl.clear_background(BACKGROUND)
    _draw_net()
    _draw_score(game)
    _draw_players(game)
    _draw_labels()
    _draw_overlay(game)
    rl.end_drawing()


def _draw_net():
    for y in range(18, HEIGHT, 34):
        rl.draw_rectangle(WIDTH // 2 - 2, y, 4, 18, MUTED)


def _draw_score(game):
    rl.draw_text(str(game.blue.score), WIDTH // 2 - 110, 38, 48, BLUE)
    rl.draw_text(str(game.red.score), WIDTH // 2 + 75, 38, 48, RED)


def _draw_players(game):
    rl.draw_rectangle(int(game.blue.x), int(game.blue.y), PADDLE_WIDTH, PADDLE_HEIGHT, BLUE)
    rl.draw_rectangle(int(game.red.x), int(game.red.y), PADDLE_WIDTH, PADDLE_HEIGHT, RED)
    rl.draw_circle(int(game.ball.x), int(game.ball.y), BALL_RADIUS, WHITE)


def _draw_labels():
    rl.draw_text("BLUE AI  •  predictive", 30, HEIGHT - 38, 17, BLUE)
    rl.draw_text("SPACE pause   R restart   ESC quit", WIDTH // 2 - 153, HEIGHT - 38, 16, MUTED)
    rl.draw_text("reactive  •  RED AI", WIDTH - 185, HEIGHT - 38, 17, RED)


def _draw_overlay(game):
    if game.paused and not game.winner:
        _center("PAUSED", 36, WHITE, HEIGHT // 2 - 22)
    elif game.winner:
        _center(game.winner + " WINS!", 42, WHITE, HEIGHT // 2 - 50)
        _center("Press R to play again", 20, MUTED, HEIGHT // 2 + 8)


def _center(text, size, color, y):
    x = WIDTH // 2 - rl.measure_text(text, size) // 2
    rl.draw_text(text, x, y, size, color)
