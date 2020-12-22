from collections import deque
from typing import Deque, Tuple


def parse_decks(text: str) -> Tuple[Deque[int], Deque[int]]:
    player_cards = {
        1: deque(),
        2: deque(),
    }
    current_player = None
    for line in text.splitlines():
        if line == "Player 1:":
            current_player = 1
        elif line == "Player 2:":
            current_player = 2
        elif line == "":
            continue
        else:
            assert current_player is not None
            player_cards[current_player].append(int(line))
    return player_cards[1], player_cards[2]
