from collections import defaultdict
from .shared import parse_instructions, execute_instruction, matrix_to_string, MATRIX_HEIGHT, MATRIX_WIDTH


def calculate(text: str) -> str:
    matrix = defaultdict(lambda: False)
    for instruction in parse_instructions(text):
        execute_instruction(matrix, MATRIX_WIDTH, MATRIX_HEIGHT, instruction)
    return "\n" + matrix_to_string(matrix, MATRIX_WIDTH, MATRIX_HEIGHT)
