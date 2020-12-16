import re

from enum import Enum
from typing import Iterable, NamedTuple, Sequence


RE_INSTRUCTION = re.compile(r"^(acc|jmp|nop) ([+\-]\d+)$")


class InstructionType(Enum):
    ACC = "acc"
    JMP = "jmp"
    NOP = "nop"


class Instruction(NamedTuple):
    type: InstructionType
    offset: int


def parse_instructions(text: str) -> Iterable[Instruction]:
    for line in text.splitlines():
        m = RE_INSTRUCTION.match(line)
        assert m is not None

        yield Instruction(InstructionType(m.group(1)), int(m.group(2)))


Instructions = Sequence[Instruction]


class Cpu(object):
    def __init__(self, instructions: Instructions):
        self.instructions = instructions
        self.accumulator = 0
        self.instruction_pointer = 0

    def step(self):
        instruction = self.instructions[self.instruction_pointer]
        if instruction.type == InstructionType.NOP:
            self.instruction_pointer += 1
        elif instruction.type == InstructionType.JMP:
            assert instruction.offset != 0
            self.instruction_pointer += instruction.offset
        elif instruction.type == InstructionType.ACC:
            self.accumulator += instruction.offset
            self.instruction_pointer += 1
        else:
            raise RuntimeError("unknown instruction")
