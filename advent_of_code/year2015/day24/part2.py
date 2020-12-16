from itertools import combinations
from .shared import parse_packages, quantum_entanglement


def calculate(text: str) -> int:
    packages = tuple(parse_packages(text))
    single_group_sum = sum(packages) // 4

    # find the smallest group
    for i in range(1, len(packages)):
        first_group_combos = {x for x in combinations(packages, i) if sum(x) == single_group_sum}
        if len(first_group_combos) > 0:
            break

    # return the minimum quantum entanglement of the possible combinations
    return min(quantum_entanglement(c) for c in first_group_combos)


puzzle = """
1
2
3
4
5
7
8
9
10
11
""".strip()
assert calculate(puzzle) == 44
