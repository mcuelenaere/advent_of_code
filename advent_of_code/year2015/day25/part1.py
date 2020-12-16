from typing import Iterable, Tuple

from .shared import parse_puzzle


def code_generator() -> Iterable[int]:
    code = 20151125
    while True:
        yield code
        code *= 252533
        code %= 33554393


def diagonal_generator() -> Iterable[Tuple[int, int]]:
    x = 1
    y = 1
    while True:
        yield x, y
        x += 1
        y -= 1
        if y == 0:
            y = x
            x = 1


def calculate(puzzle: str) -> int:
    requested_row, requested_column = parse_puzzle(puzzle)
    diagonals = diagonal_generator()
    codes = code_generator()
    while True:
        column, row = next(diagonals)
        code = next(codes)

        if row == requested_row and column == requested_column:
            return code


assert (
    calculate("To continue, please consult the code grid in the manual.  Enter the code at row 2, column 4.") == 7726640
)
assert (
    calculate("To continue, please consult the code grid in the manual.  Enter the code at row 5, column 4.") == 6899651
)
assert (
    calculate("To continue, please consult the code grid in the manual.  Enter the code at row 6, column 6.")
    == 27995004
)
