from collections import defaultdict

from .shared import (
    MATRIX_HEIGHT,
    MATRIX_WIDTH,
    execute_instruction,
    matrix_to_string,
    parse_instructions,
)


def calculate(text: str) -> str:
    matrix = defaultdict(lambda: False)
    for instruction in parse_instructions(text):
        execute_instruction(matrix, MATRIX_WIDTH, MATRIX_HEIGHT, instruction)
    return "\n" + matrix_to_string(matrix, MATRIX_WIDTH, MATRIX_HEIGHT)
