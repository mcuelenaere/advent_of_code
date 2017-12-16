def calculate(x: str) -> int:
    x = x + x[0]

    return sum(int(a) for a, b in zip(x, x[1:]) if a == b)


testcases = (
    ('1122', 3),
    ('1111', 4),
    ('1234', 0),
    ('91212129', 9),
)
for puzzle, expected_answer in testcases:
    assert calculate(puzzle) == expected_answer
