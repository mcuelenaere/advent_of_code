try:
    from .shared_native import perform_rounds
except ImportError:
    from .shared import perform_rounds


def calculate(text: str, moves: int = 100) -> str:
    cups = list(map(int, text))
    cups = perform_rounds(cups, moves)
    return "".join(map(str, cups[1:]))


assert calculate("389125467", 10) == "92658374"
assert calculate("389125467", 100) == "67384529"
