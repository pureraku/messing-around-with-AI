"""Rock-paper-scissors rules and round results."""

from dataclasses import dataclass

MOVES = ("rock", "paper", "scissors")
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


@dataclass(frozen=True)
class RoundResult:
    player_move: str
    ai_move: str
    outcome: str


def decide_winner(player_move, ai_move):
    """Return 'player', 'ai', or 'tie'."""
    if player_move == ai_move:
        return "tie"
    return "player" if BEATS[player_move] == ai_move else "ai"


def play_round(player_move, ai_move):
    if player_move not in MOVES:
        raise ValueError(f"Unknown move: {player_move}")
    if ai_move not in MOVES:
        raise ValueError(f"Unknown move: {ai_move}")
    return RoundResult(player_move, ai_move, decide_winner(player_move, ai_move))
