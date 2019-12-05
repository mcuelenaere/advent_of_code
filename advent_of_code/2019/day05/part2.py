from .shared import evaluate


def calculate(text: str) -> int:
    instructions = list(map(int, text.strip().split(',')))
    output = evaluate(instructions, 5)
    return output
