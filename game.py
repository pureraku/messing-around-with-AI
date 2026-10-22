"""Game state, ball physics, collisions and scoring."""

import math
import random

from bot import move_blue, move_red
from entities import Ball, create_paddles
from settings import (
    BALL_MAX_SPEED, BALL_RADIUS, BALL_SPEED, HEIGHT, PADDLE_BOUNCE_JITTER,
    PADDLE_HEIGHT, PADDLE_WIDTH, SERVE_ANGLE_RANGE, WALL_BOUNCE_JITTER,
    WIDTH, WINNING_SCORE,
)


class PongGame:
    def __init__(self):
        self.blue, self.red = create_paddles()
        self.ball = Ball()
        self.paused = False
        self.winner = None
        self._serve(random.choice((-1, 1)))

    def _serve(self, direction):
        angle = random.uniform(-SERVE_ANGLE_RANGE, SERVE_ANGLE_RANGE)
        self.ball = Ball(
            WIDTH / 2,
            HEIGHT / 2,
            direction * BALL_SPEED * math.cos(angle),
            BALL_SPEED * math.sin(angle),
        )

    def update(self, dt):
        if self.paused or self.winner:
            return

        if self.ball.x < WIDTH / 2:
            move_blue(self.blue, self.ball, dt)
        else:
            move_red(self.red, self.ball, dt)

        self.ball.x += self.ball.vx * dt
        self.ball.y += self.ball.vy * dt
        self._wall_collision()
        self._paddle_collision(self.blue, left=True)
        self._paddle_collision(self.red, left=False)
        self._check_point()

    def _wall_collision(self):
        ball = self.ball
        if ball.y - BALL_RADIUS < 0:
            ball.y = BALL_RADIUS
            ball.vy = abs(ball.vy)
            ball.vx += random.uniform(-WALL_BOUNCE_JITTER, WALL_BOUNCE_JITTER) * BALL_SPEED
        elif ball.y + BALL_RADIUS > HEIGHT:
            ball.y = HEIGHT - BALL_RADIUS
            ball.vy = -abs(ball.vy)
            ball.vx += random.uniform(-WALL_BOUNCE_JITTER, WALL_BOUNCE_JITTER) * BALL_SPEED

    def _paddle_collision(self, paddle, left):
        ball = self.ball
        crosses_face = (
            ball.x - BALL_RADIUS <= paddle.x + PADDLE_WIDTH
            if left else ball.x + BALL_RADIUS >= paddle.x
        )
        overlaps = (
            ball.y + BALL_RADIUS >= paddle.y
            and ball.y - BALL_RADIUS <= paddle.y + PADDLE_HEIGHT
        )
        toward = ball.vx < 0 if left else ball.vx > 0
        if not (crosses_face and overlaps and toward):
            return

        impact = (ball.y - (paddle.y + PADDLE_HEIGHT / 2)) / (PADDLE_HEIGHT / 2)
        impact = max(-1.0, min(1.0, impact + random.uniform(
            -PADDLE_BOUNCE_JITTER, PADDLE_BOUNCE_JITTER
        )))
        ball.vx = abs(ball.vx) if left else -abs(ball.vx)
        ball.vy = impact * BALL_SPEED
        self._increase_speed()
        ball.x = (
            paddle.x + PADDLE_WIDTH + BALL_RADIUS
            if left else paddle.x - BALL_RADIUS
        )

    def _increase_speed(self):
        ball = self.ball
        current = math.hypot(ball.vx, ball.vy)
        target = min(current * 1.08, BALL_MAX_SPEED)
        factor = target / max(current, 1)
        ball.vx *= factor
        ball.vy *= factor

    def _check_point(self):
        if self.ball.x + BALL_RADIUS < 0:
            self._award(self.red, direction=-1)
        elif self.ball.x - BALL_RADIUS > WIDTH:
            self._award(self.blue, direction=1)

    def _award(self, player, direction):
        player.score += 1
        if player.score >= WINNING_SCORE:
            self.winner = "BLUE" if player is self.blue else "RED"
        else:
            self._serve(direction)

    def restart(self):
        self.blue.score = self.red.score = 0
        self.blue.y = self.red.y = (HEIGHT - PADDLE_HEIGHT) / 2
        self.paused = False
        self.winner = None
        self._serve(random.choice((-1, 1)))
