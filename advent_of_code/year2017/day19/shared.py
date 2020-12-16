from typing import Iterator, List, Tuple


TextMatrix = List[List[str]]


def as_matrix(text: str) -> TextMatrix:
    return list(list(x) for x in text.splitlines())


def find_starting_position(m: TextMatrix) -> Tuple[int, int]:
    return m[0].index("|"), 0


def follow_path(m: TextMatrix) -> Iterator[str]:
    x, y = find_starting_position(m)
    x_speed, y_speed = 0, 1

    c = m[y][x]
    while c != " ":
        x += x_speed
        y += y_speed
        c = m[y][x]

        if c == "+":
            # switch directions, in a 90-degree angle
            if x_speed != 0:
                x_speed = 0
                y_speed = 1 if y + 1 < len(m) and m[y + 1][x] != " " else -1
            elif y_speed != 0:
                y_speed = 0
                x_speed = 1 if x + 1 < len(m[y]) and m[y][x + 1] != " " else -1

        yield c
