import re

from typing import Iterator, NamedTuple, Tuple, Union


IHlf = NamedTuple("IHlf", register=str)
ITpl = NamedTuple("ITpl", register=str)
IInc = NamedTuple("IInc", register=str)
IJmp = NamedTuple("IJmp", jump_offset=int)
IJie = NamedTuple("IJie", cnd_register=str, jump_offset=int)
IJio = NamedTuple("IJio", cnd_register=str, jump_offset=int)
Instruction = Union[IHlf, ITpl, IInc, IJmp, IJie, IJio]


REGEXES = (
    (re.compile(r"^hlf (?P<register>[a-b])$"), IHlf),
    (re.compile(r"^tpl (?P<register>[a-b])$"), ITpl),
    (re.compile(r"^inc (?P<register>[a-b])$"), IInc),
    (re.compile(r"^jmp (?P<jump_offset>[+-]?\d+)$"), IJmp),
    (re.compile(r"^jie (?P<cnd_register>[a-b]), (?P<jump_offset>[+-]?\d+)$"), IJie),
    (re.compile(r"^jio (?P<cnd_register>[a-b]), (?P<jump_offset>[+-]?\d+)$"), IJio),
)


def try_int(x: str) -> Union[str, int]:
    try:
        return int(x)
    except ValueError:
        return x


def parse_instructions(text: str) -> Iterator[Instruction]:
    for line in text.splitlines():
        instruction = None
        for regex, instruction_type in REGEXES:
            m = regex.match(line)
            if m is not None:
                args = {k: try_int(v) for k, v in m.groupdict().items()}
                instruction = instruction_type(**args)
                break

        if instruction is not None:
            yield instruction
        else:
            raise ValueError(f'Could not parse line "{line}"')


class Processor(object):
    def __init__(self, instructions: Tuple[Instruction, ...]):
        self.instructions = instructions
        self.instruction_offset = 0
        self.registers = {"a": 0, "b": 0}

    def _execute_instruction(self, instruction: Instruction):
        if isinstance(instruction, IHlf):
            self.registers[instruction.register] //= 2
            self.instruction_offset += 1
        elif isinstance(instruction, ITpl):
            self.registers[instruction.register] *= 3
            self.instruction_offset += 1
        elif isinstance(instruction, IInc):
            self.registers[instruction.register] += 1
            self.instruction_offset += 1
        elif isinstance(instruction, IJmp):
            self.instruction_offset += instruction.jump_offset
        elif isinstance(instruction, IJie):
            cnd_value = self.registers[instruction.cnd_register]
            if cnd_value % 2 == 0:
                self.instruction_offset += instruction.jump_offset
            else:
                self.instruction_offset += 1
        elif isinstance(instruction, IJio):
            cnd_value = self.registers[instruction.cnd_register]
            if cnd_value == 1:
                self.instruction_offset += instruction.jump_offset
            else:
                self.instruction_offset += 1
        else:
            raise ValueError(f"Unknown instruction {instruction}")

    def execute_step(self):
        self._execute_instruction(self.instructions[self.instruction_offset])
