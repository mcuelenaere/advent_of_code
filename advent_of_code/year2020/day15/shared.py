from typing import Sequence


try:
    from .shared_native import play_memory_game
except ImportError:

    def play_memory_game(numbers: Sequence[int], max_turn: int) -> int:
        numbers_history = [0] * max_turn
        for i in range(1, len(numbers) + 1):
            numbers_history[numbers[i - 1]] = i

        last_number = numbers[-1]
        for turn in range(len(numbers), max_turn):
            numbers_history[last_number], last_number = (
                turn,
                turn - numbers_history[last_number] if numbers_history[last_number] != 0 else 0,
            )

        return last_number
