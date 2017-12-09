import math


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


def get_adjacent_sum(matrix, x, y):
    n = len(matrix)
    s = 0
    offsets = (
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
    )
    for dx, dy in offsets:
        _x = x + dx
        _y = y + dy
        if _x >= n or _x < 0:
            continue
        elif _y >= n or _y < 0:
            continue
        s += matrix[_x][_y]
    return s


def print_matrix(matrix):
    print("\n".join(" ".join("%04d" % x for x in row) for row in matrix))
    print("\n")


def calculate(text: str) -> int:
    number = int(text)

    n = int(math.ceil(math.sqrt(number)))
    matrix = list([0] * n for _ in range(n))

    # set initial value
    matrix[n // 2][n // 2] = 1

    it = bruteforce_iterator()
    for _ in range(number):
        y, x = next(it)

        # position (x, y) globally
        x = -x
        x += n // 2
        y += n // 2

        # set the value in the matrix to the adjacent sum
        val = matrix[x][y] = get_adjacent_sum(matrix, x, y)
        #print_matrix(matrix)
        if val > number:
            return val
