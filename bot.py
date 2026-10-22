"""Distinct rule-based controllers; a future lesson can replace either one."""

import random

from settings import BALL_RADIUS, HEIGHT, PADDLE_HEIGHT, PADDLE_SPEED, WIDTH


def move_blue(paddle, ball, dt):
    """Blue predicts the ball's intercept, including reflections off the walls."""
    if ball.vx >= 0:
        return
    target = predict_intercept(ball, paddle.x)
    _move(paddle, target, dt, PADDLE_SPEED * 1.08)


def move_red(paddle, ball, dt):
    """Red uses a delayed, noisy observation and a slower tracking speed."""
    if ball.vx <= 0:
        return
    estimated_y = ball.y + ball.vy * 0.12 + random.uniform(-28, 28)
    _move(paddle, estimated_y, dt, PADDLE_SPEED * 0.86)


def predict_intercept(ball, paddle_x):
    """Estimate the ball's y at paddle_x after any number of wall bounces."""
    if abs(ball.vx) < 1:
        return ball.y
    seconds = max(0.0, (paddle_x - ball.x) / ball.vx)
    projected = ball.y + ball.vy * seconds
    span = HEIGHT - 2 * BALL_RADIUS
    folded = (projected - BALL_RADIUS) % (2 * span)
    if folded > span:
        folded = 2 * span - folded
    return folded + BALL_RADIUS


def _move(paddle, target_ball_y, dt, speed):
    target_y = target_ball_y - PADDLE_HEIGHT / 2
    delta = target_y - paddle.y
    step = max(-speed * dt, min(speed * dt, delta))
    paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, paddle.y + step))
