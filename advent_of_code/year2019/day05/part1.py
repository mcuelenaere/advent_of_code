from .shared import evaluate, parse_instructions


def calculate(text: str) -> int:
    instructions = parse_instructions(text)
    output = evaluate(instructions, 1)
    return output
