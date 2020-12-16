from itertools import chain

from .shared import (
    CharacterType,
    all_shop_combinations,
    build_character_from_items,
    calculate_winner,
    parse_character,
)


def calculate(text: str) -> int:
    enemy = parse_character(text)

    # brute force all combinations
    highest_cost = None
    for weapons, armors, rings in all_shop_combinations():
        # build character
        player, total_cost = build_character_from_items(hit_points=100, items=chain(weapons, armors, rings))

        # calculate winner
        winner = calculate_winner(player, enemy)

        # find lowest cost
        if winner == CharacterType.ENEMY and (highest_cost is None or total_cost > highest_cost):
            highest_cost = total_cost

    return highest_cost
