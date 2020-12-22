from .shared import parse_decks


def calculate(text: str) -> int:
    player_1, player_2 = parse_decks(text)
    while len(player_1) > 0 and len(player_2) > 0:
        a, b = player_1.popleft(), player_2.popleft()
        if a > b:
            player_1.extend((a, b))
        else:
            player_2.extend((b, a))
    winning_player = player_1 if len(player_1) > 0 else player_2
    return sum(i * x for i, x in enumerate(reversed(winning_player), start=1))


puzzle = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
assert calculate(puzzle) == 306
