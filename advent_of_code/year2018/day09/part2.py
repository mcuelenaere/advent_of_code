from .shared import calculate_winning_score, parse_assignment


def calculate(text: str) -> int:
    player_count, last_marble_worth = parse_assignment(text)
    return calculate_winning_score(player_count, last_marble_worth * 100)
