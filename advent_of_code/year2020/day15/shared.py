from collections import defaultdict, deque
from typing import Sequence


def play_memory_game(numbers: Sequence[int], max_turn: int) -> int:
    numbers_history = defaultdict(lambda: deque(maxlen=2))

    # seed spoken_numbers
    for i in range(1, len(numbers) + 1):
        numbers_history[numbers[i - 1]].append(i)

    last_number = numbers[-1]
    for turn in range(len(numbers) + 1, max_turn + 1):
        if len(numbers_history[last_number]) < 2:
            last_number = 0
        else:
            a, b = numbers_history[last_number]
            last_number = b - a
        numbers_history[last_number].append(turn)

    return last_number
