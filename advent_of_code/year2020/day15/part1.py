from .shared import play_memory_game


def calculate(text: str) -> int:
    numbers = tuple(map(int, text.split(",")))
    return play_memory_game(numbers, 2020)


assert calculate("0,3,6") == 436
assert calculate("1,3,2") == 1
assert calculate("2,1,3") == 10
assert calculate("1,2,3") == 27
assert calculate("2,3,1") == 78
assert calculate("3,2,1") == 438
assert calculate("3,1,2") == 1836
