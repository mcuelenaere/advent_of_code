import operator
import re

from collections import defaultdict
from typing import Iterable, Union


RE_INSTRUCTION_LINE = re.compile(r"(\w+) (inc|dec) ([\d\-]+) if (\w+) ([<>=!]+) ([\d\-]+)")


def parse_instructions(lines: Iterable[str]) -> Iterable[dict]:
    for line in lines:
        m = RE_INSTRUCTION_LINE.match(line)
        if m is None:
            raise ValueError(f'Could not parse "{line}"')
        yield {
            "operation": {
                "register": m.group(1),
                "operator": m.group(2),
                "operand": int(m.group(3)),
            },
            "condition": {
                "register": m.group(4),
                "operator": m.group(5),
                "operand": int(m.group(6)),
            },
        }


class Cpu(object):
    OPERATORS = {
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
        "inc": operator.add,
        "dec": operator.sub,
    }

    def __init__(self):
        self.registers = defaultdict(int)
        self.max_value = 0

    def evaluate_instruction(self, register: str, operator: str, operand: int) -> Union[bool, int]:
        current_value = self.registers[register]
        return self.OPERATORS[operator](current_value, operand)

    def execute_instruction(self, instruction: dict):
        condition = instruction["condition"]
        result = self.evaluate_instruction(condition["register"], condition["operator"], condition["operand"])
        if not result:
            # don't execute this instruction
            return

        # calculate result of this instruction
        operation = instruction["operation"]
        result = self.evaluate_instruction(operation["register"], operation["operator"], operation["operand"])

        # store result
        self.registers[operation["register"]] = result
