"""Terminal prompts and friendly round summaries."""

from rps import MOVES


ALIASES = {
    "r": "rock", "rock": "rock",
    "p": "paper", "paper": "paper",
    "s": "scissors", "scissors": "scissors",
}


def ask_for_move():
    while True:
        answer = input("Your move [r]ock, [p]aper, [s]cissors (or q to quit): ").strip().lower()
        if answer in ("q", "quit", "exit"):
            return None
        if answer in ALIASES:
            return ALIASES[answer]
        print("I didn't recognize that move. Try r, p, s, or q.")


def show_round(number, player_move, ai_move, outcome):
    labels = {"player": "You win!", "ai": "AI wins!", "tie": "Tie round."}
    print(f"Round {number}: you played {player_move}; AI played {ai_move}. {labels[outcome]}")


def show_score(player_score, ai_score, ties):
    print(f"Score — You: {player_score} | AI: {ai_score} | Ties: {ties}")


def show_learning(move_counts):
    if not move_counts:
        return
    learned = ", ".join(f"{move}: {move_counts.get(move, 0)}" for move in MOVES)
    print(f"Opponent move history — {learned}")
