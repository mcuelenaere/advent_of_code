from .shared import parse_text, find_connected_programs


def calculate(text: str) -> int:
    configuration = parse_text(text)
    connected_programs = tuple(find_connected_programs(configuration, 0))
    return len(connected_programs)


puzzle = """
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
""".strip()
assert calculate(puzzle) == 6
