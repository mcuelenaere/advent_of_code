import re
from typing import Iterable, Tuple


def parse_specifications(text: str) -> Iterable[Tuple[int, int, int]]:
    re_whitespace = re.compile('\s+')
    for line in text.splitlines():
        line = line.strip()
        yield tuple(int(dim) for dim in re_whitespace.split(line))


def is_valid_triangle(a: int, b: int, c: int) -> bool:
    if a + b <= c:
        return False
    elif b + c <= a:
        return False
    elif a + c <= b:
        return False
    else:
        return True
