from .shared import calculate_winning_score, parse_assignment


def calculate(text: str) -> int:
    player_count, last_marble_worth = parse_assignment(text)
    return calculate_winning_score(player_count, last_marble_worth)


assert calculate("9 players; last marble is worth 25 points") == 32
assert calculate("10 players; last marble is worth 1618 points") == 8317
assert calculate("13 players; last marble is worth 7999 points") == 146373
assert calculate("17 players; last marble is worth 1104 points") == 2764
assert calculate("21 players; last marble is worth 6111 points") == 54718
assert calculate("30 players; last marble is worth 5807 points") == 37305
