import re

from typing import Dict, Iterable, NamedTuple, Tuple, Union


IRect = NamedTuple("Rect", width=int, height=int)
IRotateRow = NamedTuple("RotateRow", row=int, amount=int)
IRotateColumn = NamedTuple("RotateColumn", column=int, amount=int)
Instruction = Union[IRect, IRotateRow, IRotateColumn]
Matrix = Dict[Tuple[int, int], bool]

RE_RECT = re.compile(r"^rect (\d+)x(\d+)$")
RE_ROTATE_ROW = re.compile(r"^rotate row y=(\d+) by (\d+)$")
RE_ROTATE_COLUMN = re.compile(r"^rotate column x=(\d+) by (\d+)$")
MATRIX_WIDTH = 50
MATRIX_HEIGHT = 6


def parse_instructions(text: str) -> Iterable[Instruction]:
    for line in text.splitlines():
        m = RE_RECT.match(line)
        if m:
            yield IRect(width=int(m.group(1)), height=int(m.group(2)))
        m = RE_ROTATE_ROW.match(line)
        if m:
            yield IRotateRow(row=int(m.group(1)), amount=int(m.group(2)))
        m = RE_ROTATE_COLUMN.match(line)
        if m:
            yield IRotateColumn(column=int(m.group(1)), amount=int(m.group(2)))


def execute_instruction(matrix: Matrix, screen_width: int, screen_height: int, instruction: Instruction):
    if isinstance(instruction, IRect):
        for x in range(instruction.width):
            for y in range(instruction.height):
                matrix[(x, y)] = True
    elif isinstance(instruction, IRotateRow):
        old_row = [matrix[(x, instruction.row)] for x in range(screen_width)]
        for x in range(screen_width):
            matrix[(x, instruction.row)] = old_row[(x - instruction.amount) % screen_width]
    elif isinstance(instruction, IRotateColumn):
        old_col = [matrix[(instruction.column, y)] for y in range(screen_height)]
        for y in range(screen_height):
            matrix[(instruction.column, y)] = old_col[(y - instruction.amount) % screen_height]


def matrix_to_string(matrix: Matrix, screen_width: int, screen_height: int) -> str:
    s = ""
    for y in range(screen_height):
        s += "".join("#" if matrix[(x, y)] else "." for x in range(screen_width)) + "\n"
    return s
