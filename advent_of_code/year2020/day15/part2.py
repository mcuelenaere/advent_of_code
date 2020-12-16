from .shared import play_memory_game


def calculate(text: str) -> int:
    numbers = tuple(map(int, text.split(",")))
    return play_memory_game(numbers, 30_000_000)


#assert calculate("0,3,6") == 175594
#assert calculate("1,3,2") == 2578
#assert calculate("2,1,3") == 3544142
#assert calculate("1,2,3") == 261214
#assert calculate("2,3,1") == 6895259
#assert calculate("3,2,1") == 18
#assert calculate("3,1,2") == 362
