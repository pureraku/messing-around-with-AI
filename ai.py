"""Adaptive opponent model for rock-paper-scissors."""

from collections import Counter
import random

from rps import MOVES


class AdaptiveAI:
    """Predict the opponent's most frequent move and play its counter."""

    def __init__(self, rng=None):
        self.move_counts = Counter()
        self.rng = rng or random.Random()

    def choose_move(self):
        # Explore randomly until there is enough history to see a pattern.
        if sum(self.move_counts.values()) < 3:
            return self.rng.choice(MOVES)

        highest_count = max(self.move_counts.values())
        most_common = [move for move in MOVES if self.move_counts[move] == highest_count]
        predicted_move = self.rng.choice(most_common)
        return {"rock": "paper", "paper": "scissors", "scissors": "rock"}[predicted_move]

    def observe(self, opponent_move):
        if opponent_move not in MOVES:
            raise ValueError(f"Unknown move: {opponent_move}")
        self.move_counts[opponent_move] += 1
