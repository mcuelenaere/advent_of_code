from .shared import find_possible_routes, parse_lines


def calculate(text: str) -> int:
    distances = parse_lines(text)
    return max(distance for route, distance in find_possible_routes(distances))


puzzle = """
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
""".strip()
assert calculate(puzzle) == 982
