import re

from typing import Dict, Iterator, NamedTuple, Tuple, Union


ISet = NamedTuple("ISet", dst_register=str, src=Union[int, str])
ISub = NamedTuple("ISub", dst_register=str, src=Union[int, str])
IMul = NamedTuple("IMul", dst_register=str, src=Union[int, str])
IJnz = NamedTuple("IJnz", cnd=Union[int, str], jump_offset=int)
Instruction = Union[ISet, ISub, IMul, IJnz]


REGEXES = (
    (re.compile(r"^set (?P<dst_register>[a-h]) (?P<src>(?:-?\d+|[a-h]))$"), ISet),
    (re.compile(r"^sub (?P<dst_register>[a-h]) (?P<src>(?:-?\d+|[a-h]))$"), ISub),
    (re.compile(r"^mul (?P<dst_register>[a-h]) (?P<src>(?:-?\d+|[a-h]))$"), IMul),
    (re.compile(r"^jnz (?P<cnd>(?:-?\d+|[a-h])) (?P<jump_offset>-?\d+)$"), IJnz),
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


class Coprocessor(object):
    def __init__(self, instructions: Tuple[Instruction, ...]):
        self.instructions = instructions
        self.instruction_offset = 0
        self.registers = {chr(c): 0 for c in range(ord("a"), ord("h") + 1)}

    def _execute_instruction(self, instruction: Instruction):
        if isinstance(instruction, ISet):
            src_value = instruction.src if isinstance(instruction.src, int) else self.registers[instruction.src]
            self.registers[instruction.dst_register] = src_value
            self.instruction_offset += 1
        elif isinstance(instruction, ISub):
            src_value = instruction.src if isinstance(instruction.src, int) else self.registers[instruction.src]
            self.registers[instruction.dst_register] -= src_value
            self.instruction_offset += 1
        elif isinstance(instruction, IMul):
            src_value = instruction.src if isinstance(instruction.src, int) else self.registers[instruction.src]
            self.registers[instruction.dst_register] *= src_value
            self.instruction_offset += 1
        elif isinstance(instruction, IJnz):
            cnd_value = instruction.cnd if isinstance(instruction.cnd, int) else self.registers[instruction.cnd]
            self.instruction_offset += instruction.jump_offset if cnd_value != 0 else 1
        else:
            raise ValueError(f"Unknown instruction {instruction}")

    def execute_step(self):
        self._execute_instruction(self.instructions[self.instruction_offset])


# NOTE: this is just here for illustrative purpose, the complexity of the puzzle is still too high, even
#       if you run it on a faster interpreter
def aot_instructions(registers: Dict[str, int], instructions: Tuple[Instruction, ...]) -> callable:
    from byteasm import FunctionBuilder

    b = FunctionBuilder()
    for register, value in registers.items():
        b.emit_load_const(value)
        b.emit_store_fast(register)
        b.inc_line_number()

    for instruction_number, instruction in enumerate(instructions):
        b.emit_label(f"i_{instruction_number}")
        if isinstance(instruction, ISet):
            if isinstance(instruction.src, int):
                b.emit_load_const(instruction.src)
            else:
                b.emit_load_fast(instruction.src)
            b.emit_store_fast(instruction.dst_register)
        elif isinstance(instruction, ISub):
            b.emit_load_fast(instruction.dst_register)
            if isinstance(instruction.src, int):
                b.emit_load_const(instruction.src)
            else:
                b.emit_load_fast(instruction.src)
            b.emit_inplace_subtract()
            b.emit_store_fast(instruction.dst_register)
        elif isinstance(instruction, IMul):
            b.emit_load_fast(instruction.dst_register)
            if isinstance(instruction.src, int):
                b.emit_load_const(instruction.src)
            else:
                b.emit_load_fast(instruction.src)
            b.emit_inplace_multiply()
            b.emit_store_fast(instruction.dst_register)
        elif isinstance(instruction, IJnz):
            if isinstance(instruction.cnd, int):
                b.emit_load_const(instruction.cnd)
            else:
                b.emit_load_fast(instruction.cnd)
            b.emit_load_const(0)
            b.emit_compare_ne()
            b.emit_pop_jump_if_true(f"i_{instruction_number + instruction.jump_offset}")
        else:
            raise ValueError(f"Unknown instruction {instruction}")
        b.inc_line_number()

    b.emit_label(f"i_{len(instructions)}")
    b.emit_load_global("locals")
    b.emit_call_function(0)
    b.emit_return_value()
    b.inc_line_number()

    return b.make("f")
