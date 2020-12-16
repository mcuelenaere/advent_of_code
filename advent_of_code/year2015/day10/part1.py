from .shared import look_and_say


def calculate(text: str) -> int:
    for _ in range(40):
        text = look_and_say(text)
    return len(text)
