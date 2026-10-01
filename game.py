import random
from logic import feedback


DIFFICULTIES = {
    "1": {"name": "Easy",   "length": 3, "symbols": 4, "turns": 12},
    "2": {"name": "Medium", "length": 4, "symbols": 6, "turns": 10},
    "3": {"name": "Hard",   "length": 5, "symbols": 8, "turns": 8},
}


class Mastermind:
    def __init__(self, difficulty="2"):
        config = DIFFICULTIES.get(difficulty, DIFFICULTIES["2"])
        self.name = config["name"]
        self.length = config["length"]
        self.symbols = config["symbols"]
        self.turns_total = config["turns"]
        self.turns = self.turns_total
        self.symbol_set = "".join(str(i) for i in range(1, self.symbols + 1))
        self.code = self._generate_code()
        self.history = []
        self.game_over = False
        self.won = False

    def _generate_code(self):
        return [str(random.randint(1, self.symbols)) for _ in range(self.length)]

    def validate_guess(self, raw):
        """Return (is_valid, error_message) for a raw guess string."""
        if len(raw) != self.length:
            return False, f"Enter exactly {self.length} digits."
        if any(ch not in self.symbol_set for ch in raw):
            return False, f"Digits must be from 1 to {self.symbols}."
        return True, ""

    def format_history(self):
        """Return a printable guess-history table."""
        if not self.history:
            return "No guesses yet."
        header = f"{'Turn':<5} | {'Guess':<{self.length}} | Exact | Partial"
        lines = [header, "-" * len(header)]
        for turn, (guess, exact, partial) in enumerate(self.history, start=1):
            lines.append(f"{turn:<5} | {guess:<{self.length}} | {exact:<5} | {partial}")
        return "\n".join(lines)

    def _end_game(self, won):
        self.game_over = True
        self.won = won
        if won:
            print("You cracked the code!")
        else:
            print(f"You lost! The code was: {''.join(self.code)}")
        print("\nGame History:\n" + self.format_history())

    def run(self):
        print(f"Mastermind ({self.name}) - guess {self.length} digits from 1 to {self.symbols}.")
        print(f"You have {self.turns_total} turns. Type 'q' to quit.\n")

        while self.turns > 0 and not self.game_over:
            print(self.format_history())
            print()
            raw = input(f"{self.turns} turns left > ").strip()

            if raw.lower() == "q":
                print("Thanks for playing!")
                return

            valid, error = self.validate_guess(raw)
            if not valid:
                print(f"Invalid guess: {error} Try again.\n")
                continue

            guess = list(raw)
            exact, partial = feedback(self.code, guess)
            self.history.append((raw, exact, partial))
            self.turns -= 1

            print(f"Exact: {exact}  Partial: {partial}\n")

            if exact == self.length:
                self._end_game(won=True)
                return

        if not self.game_over:
            self._end_game(won=False)


def choose_difficulty():
    print("Choose difficulty:")
    for key, config in DIFFICULTIES.items():
        print(
            f"  {key}. {config['name']}: "
            f"{config['length']} digits, symbols 1-{config['symbols']}, "
            f"{config['turns']} turns"
        )
    choice = input("Enter 1/2/3 (default 2): ").strip()
    return choice if choice in DIFFICULTIES else "2"


if __name__ == "__main__":
    difficulty = choose_difficulty()
    Mastermind(difficulty=difficulty).run()
