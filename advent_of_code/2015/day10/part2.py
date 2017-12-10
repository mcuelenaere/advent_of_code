from .shared import look_and_say


def calculate(text: str) -> int:
    for _ in range(50):
        text = look_and_say(text)
    return len(text)
