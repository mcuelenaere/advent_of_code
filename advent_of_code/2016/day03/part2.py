from .shared import parse_specifications, is_valid_triangle


def calculate(text: str) -> int:
    specs = tuple(parse_specifications(text))
    valid = 0
    for rows in zip(specs[::3], specs[1::3], specs[2::3]):
        columns = ((r[i] for r in rows) for i in range(3))
        valid += sum(1 for a, b, c in columns if is_valid_triangle(a, b, c))
    return valid
