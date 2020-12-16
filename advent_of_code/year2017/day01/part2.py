def calculate(x: str) -> int:
    assert len(x) % 2 == 0
    offset = len(x) // 2

    s = 0
    for idx, a in enumerate(x):
        if x[(idx + offset) % len(x)] == a:
            s += int(a)

    return s


testcases = (
    ("1212", 6),
    ("1221", 0),
    ("123425", 4),
    ("123123", 12),
    ("12131415", 4),
)
for puzzle, expected_answer in testcases:
    assert calculate(puzzle) == expected_answer
