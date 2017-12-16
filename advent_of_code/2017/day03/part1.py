def bruteforce_iterator():
    position = [0, 0]
    # start position
    yield position

    i = 1
    while True:
        for _ in range(i):
            # move right
            position[0] += 1
            yield position
        for _ in range(i):
            # move up
            position[1] += 1
            yield position
        i += 1

        for _ in range(i):
            # move left
            position[0] -= 1
            yield position
        for _ in range(i):
            # move down
            position[1] -= 1
            yield position
        i += 1


def calculate(text: str) -> int:
    number = int(text)
    it = bruteforce_iterator()
    for _ in range(number):
        x, y = next(it)
    return abs(x) + abs(y)


testcases = (
    ('1', 0),
    ('12', 3),
    ('23', 2),
    ('1024', 31),
)
for puzzle, expected_answer in testcases:
    assert calculate(puzzle) == expected_answer
