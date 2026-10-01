from collections import Counter


def feedback(code, guess):
    """
    Return (exact, partial) feedback for a Mastermind guess.

    - Exact: digit in the correct position.
    - Partial: correct digit but in the wrong position.

    Each position in the secret code may contribute at most once to the
    feedback. Exact matches are resolved before partial matches.
    """
    exact = sum(a == b for a, b in zip(code, guess))

    # Remove exact-match positions before counting partials so that a code
    # position is never counted twice.
    code_remaining = [a for i, a in enumerate(code) if a != guess[i]]
    guess_remaining = [b for i, b in enumerate(guess) if code[i] != b]

    code_counts = Counter(code_remaining)
    guess_counts = Counter(guess_remaining)

    partial = sum(
        min(code_counts[digit], guess_counts[digit])
        for digit in guess_counts
    )

    return exact, partial
