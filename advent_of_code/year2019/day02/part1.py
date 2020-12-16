from .shared import evaluate


def calculate(text: str) -> int:
    opcodes = list(map(int, text.strip().split(",")))
    opcodes[1] = 12
    opcodes[2] = 2
    evaluate(opcodes)
    return opcodes[0]
