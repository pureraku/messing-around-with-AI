"""Play adaptive rock-paper-scissors in the terminal."""

from ai import AdaptiveAI
from cli import ask_for_move, show_learning, show_round, show_score
from rps import play_round


def main():
    print("Rock-Paper-Scissors AI")
    print("The AI tracks your move history and tries to counter your favorite move.\n")

    ai = AdaptiveAI()
    player_score = ai_score = ties = 0
    round_number = 0

    while True:
        player_move = ask_for_move()
        if player_move is None:
            break

        ai_move = ai.choose_move()
        result = play_round(player_move, ai_move)
        ai.observe(player_move)
        round_number += 1

        show_round(round_number, result.player_move, result.ai_move, result.outcome)
        if result.outcome == "player":
            player_score += 1
        elif result.outcome == "ai":
            ai_score += 1
        else:
            ties += 1
        show_score(player_score, ai_score, ties)
        show_learning(ai.move_counts)
        print()

    print(f"Final score — You: {player_score} | AI: {ai_score} | Ties: {ties}")
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
