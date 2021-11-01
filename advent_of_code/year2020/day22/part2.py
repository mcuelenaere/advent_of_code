from collections import deque
from itertools import islice
from typing import Deque, Tuple

from .shared import parse_decks


def play_game(player_1: Deque[int], player_2: Deque[int]) -> Tuple[int, Deque[int]]:
    seen_decks_p1, seen_decks_p2 = set(), set()
    while len(player_1) > 0 and len(player_2) > 0:
        deck_p1, deck_p2 = tuple(player_1), tuple(player_2)
        if deck_p1 in seen_decks_p1 and deck_p2 in seen_decks_p2:
            # loop detected, player 1 wins
            return 1, player_1
        seen_decks_p1.add(deck_p1)
        seen_decks_p2.add(deck_p2)

        a, b = player_1.popleft(), player_2.popleft()
        if len(player_1) >= a and len(player_2) >= b:
            # playing subgame to determine winner
            winner, _ = play_game(deque(islice(player_1, 0, a)), deque(islice(player_2, 0, b)))
        else:
            winner = 1 if a > b else 2

        if winner == 1:
            player_1.extend((a, b))
        else:
            player_2.extend((b, a))

    if len(player_1) == 0:
        return 2, player_2
    else:
        return 1, player_1


def calculate(text: str) -> int:
    player_1, player_2 = parse_decks(text)
    _, winning_player = play_game(player_1, player_2)
    return sum(i * x for i, x in enumerate(reversed(winning_player), start=1))


puzzle = """Player 1:
43
19

Player 2:
2
29
14"""
assert calculate(puzzle) > 0


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
assert calculate(puzzle) == 291
