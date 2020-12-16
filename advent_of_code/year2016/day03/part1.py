from .shared import is_valid_triangle, parse_specifications


def calculate(text: str) -> int:
    valid = 0
    for a, b, c in parse_specifications(text):
        if is_valid_triangle(a, b, c):
            valid += 1
    return valid
