import re

from typing import Tuple


RE_PUZZLE = re.compile(
    r"To continue, please consult the code grid in the manual.  Enter the code at row (\d+), column (\d+)."
)


def parse_puzzle(text: str) -> Tuple[int, int]:
    m = RE_PUZZLE.match(text)
    return int(m.group(1)), int(m.group(2))
