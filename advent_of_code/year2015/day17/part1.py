from itertools import combinations

from .shared import parse_text


def calculate(text: str, total: int = 150) -> int:
    containers = tuple(parse_text(text))
    count = 0
    for container_count in range(1, len(containers) + 1):
        count += sum(1 for c in combinations(containers, container_count) if sum(c) == total)
    return count


puzzle = """
20
15
10
5
5
""".strip()
assert calculate(puzzle, 25) == 4
