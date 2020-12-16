def is_valid_passphrase(passphrase: str) -> bool:
    already_seen = set()
    for word in passphrase.split(" "):
        if word in already_seen:
            return False
        already_seen.add(word)
    return True


def calculate(text: str) -> int:
    return sum(1 for line in text.splitlines() if is_valid_passphrase(line))


testcases = (
    ("aa bb cc dd ee", True),
    ("aa bb cc dd aa", False),
    ("aa bb cc dd aaa", True),
)
for puzzle, expected_answer in testcases:
    assert is_valid_passphrase(puzzle) == expected_answer
