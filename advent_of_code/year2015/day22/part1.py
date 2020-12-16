from .shared import (
    BattleState,
    Character,
    CharacterType,
    find_win_for_lowest_spent_mana,
    parse_character,
)


def calculate(text: str) -> int:
    # create new state
    state = BattleState(
        player=Character(hit_points=50, damage_score=0, armor_score=0),
        enemy=parse_character(text),
        active_character=CharacterType.PLAYER,
        player_mana=500,
        active_effects=[],
    )

    return find_win_for_lowest_spent_mana(state)
