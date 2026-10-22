"""Application entry point."""

import pyray as rl

from game import PongGame
from renderer import draw
from settings import HEIGHT, MAX_FRAME_TIME, TARGET_FPS, WIDTH


def main():
    rl.init_window(WIDTH, HEIGHT, "Blue vs Red — AI Pong")
    rl.set_target_fps(TARGET_FPS)
    game = PongGame()
    try:
        while not rl.window_should_close():
            _handle_keys(game)
            game.update(min(rl.get_frame_time(), MAX_FRAME_TIME))
            draw(game)
    finally:
        rl.close_window()


def _handle_keys(game):
    if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE) and not game.winner:
        game.paused = not game.paused
    if rl.is_key_pressed(rl.KeyboardKey.KEY_R):
        game.restart()


if __name__ == "__main__":
    main()
