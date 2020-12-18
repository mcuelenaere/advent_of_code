from .shared import evaluate, parse_expr


def calculate(text: str) -> int:
    total = 0
    for line in text.splitlines():
        total += evaluate(parse_expr(line))
    return total


assert calculate("1 + 2 * 3 + 4 * 5 + 6") == 71
assert calculate("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert calculate("2 * 3 + (4 * 5)") == 26
assert calculate("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert calculate("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert calculate("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632
