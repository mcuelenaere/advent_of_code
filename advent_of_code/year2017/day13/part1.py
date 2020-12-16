from .shared import parse


def calculate(text: str) -> int:
    firewall = parse(text)
    score = 0
    for player_position in range(firewall.width + 1):
        if firewall.is_caught(player_position):
            score += player_position * firewall.max_depths[player_position]
        firewall.execute_step()
    return score


puzzle = """
0: 3
1: 2
4: 4
6: 4
""".strip()
assert calculate(puzzle) == 24
