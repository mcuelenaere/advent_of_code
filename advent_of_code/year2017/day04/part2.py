def is_valid_passphrase(passphrase: str) -> bool:
    already_seen = set()
    for word in passphrase.split(" "):
        word = "".join(sorted(word))
        if word in already_seen:
            return False
        already_seen.add(word)
    return True


def calculate(text: str) -> int:
    return sum(1 for line in text.splitlines() if is_valid_passphrase(line))


testcases = (
    ("abcde fghij", True),
    ("abcde xyz ecdab", False),
    ("a ab abc abd abf abj", True),
    ("iiii oiii ooii oooi oooo", True),
    ("oiii ioii iioi iiio", False),
)
for puzzle, expected_answer in testcases:
    assert is_valid_passphrase(puzzle) == expected_answer
