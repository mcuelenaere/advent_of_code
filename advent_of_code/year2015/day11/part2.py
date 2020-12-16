from .shared import find_next_valid_password


def calculate(text: str) -> str:
    first = find_next_valid_password(text)
    second = find_next_valid_password(first)
    return second
