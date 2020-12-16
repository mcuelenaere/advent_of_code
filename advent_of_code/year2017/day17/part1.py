from .shared import spinlock


def calculate(text: str) -> int:
    step_size = int(text)
    buffer = spinlock(step_size, 2017)
    return buffer[(buffer.index(2017) + 1) % len(buffer)]


assert calculate("3") == 638
