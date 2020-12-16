from .shared import calculate_bridge_strength, create_combinations, parse_text


def calculate(text: str) -> int:
    components = parse_text(text)
    combinations = tuple(create_combinations(components))
    longest_bridge = max(len(bridge) for bridge in combinations)
    max_strength = max(calculate_bridge_strength(bridge) for bridge in combinations if len(bridge) == longest_bridge)
    return max_strength


puzzle = """
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
""".strip()
assert calculate(puzzle) == 19
