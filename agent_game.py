import argparse
import re

from animal import get_random_animal
from agents import GuesserAgent, AnswererAgent


def normalized(text):
    return re.sub(r"\W+", " ", text.lower()).strip()


def is_correct_guess(guess, animal):
    return re.search(rf"\b{re.escape(normalized(animal))}\b", normalized(guess)) is not None


def yes_or_no(reply):
    return "yes" if normalized(reply).startswith(("yes", "y")) else "no"


def main():
    parser = argparse.ArgumentParser(
        description="Two AI agents play 20 questions while you watch the transcript.")
    parser.add_argument("--max-questions", type=int, default=20,
                        help="How many questions the guesser may ask (default: 20)")
    parser.add_argument("--animal",
                        help="Force a specific secret animal instead of a random one")
    args = parser.parse_args()

    animal = (args.animal or get_random_animal()).lower()
    guesser = GuesserAgent(args.max_questions)
    answerer = AnswererAgent(animal)

    print(f"Secret animal (only the answerer agent knows it): {animal}")
    print("=" * 60)

    feedback = None
    turn = 0
    try:
        while True:
            turn += 1
            kind, text = guesser.next_move(feedback)
            feedback = None
            if kind == "guess":
                print(f"[turn {turn}] Guesser guesses: {text}")
                if is_correct_guess(text, animal):
                    print(f"\nReferee: Correct! The animal was '{animal}'. "
                          f"The guesser won after {guesser.questions_asked} questions.")
                    return
                if guesser.questions_asked >= args.max_questions:
                    print(f"\nReferee: Wrong guess and no questions left. "
                          f"The guesser loses. The animal was '{animal}'.")
                    return
                print("Referee: Wrong guess.")
                feedback = "That guess is wrong, it is not the secret animal. Keep asking questions."
            else:
                if guesser.questions_asked > args.max_questions:
                    print(f"\nReferee: The guesser ran out of questions without a final "
                          f"guess. The animal was '{animal}'.")
                    return
                print(f"[turn {turn}] Guesser asks: {text}")
                reply = answerer.answer(text)
                print(f"[turn {turn}] Answerer replies: {reply}")
                feedback = f"The answer to your last question was: {yes_or_no(reply)}."
    except KeyboardInterrupt:
        print(f"\nGame stopped by monitor. The animal was '{animal}'.")


if __name__ == "__main__":
    main()