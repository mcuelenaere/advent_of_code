from .shared import find_index


def calculate(text: str) -> int:
    return find_index(text, 5)


assert calculate("abcdef") == 609043
assert calculate("pqrstuv") == 1048970
