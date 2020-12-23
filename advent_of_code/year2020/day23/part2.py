try:
    from .shared_native import perform_rounds
except ImportError:
    from .shared import perform_rounds


def calculate(text: str) -> int:
    cups = list(map(int, text))
    cups += tuple(range(max(cups) + 1, 1_000_001))
    cups = perform_rounds(cups, 10_000_000)
    return cups[1] * cups[2]


assert calculate("389125467") == 149245887792
