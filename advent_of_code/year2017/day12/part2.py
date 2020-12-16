from .shared import find_groups, parse_text


def calculate(text: str) -> int:
    configuration = parse_text(text)
    groups = tuple(find_groups(configuration))
    return len(groups)


puzzle = """
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
""".strip()
assert calculate(puzzle) == 2
