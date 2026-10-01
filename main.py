from game import Mastermind, choose_difficulty

if __name__ == "__main__":
    difficulty = choose_difficulty()
    Mastermind(difficulty=difficulty).run()
