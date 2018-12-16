import re
from typing import NamedTuple, Tuple, Dict, Callable

Registers = Tuple[int, int, int, int]
Instruction = NamedTuple('Instruction', opcode=int, input_a=int, input_b=int, output=int)
Testcase = NamedTuple('Testcase', registers_before=Registers, instruction=Instruction, registers_after=Registers)


RE_TESTCASE = re.compile(r'^Before:\s+\[([\d, ]+)\]\n([\d ]+)\nAfter:\s+\[([\d, ]+)\]$', re.MULTILINE)


def parse_puzzle(text: str):
    testcases_text, test_program_text = text.split("\n\n\n\n", 2)

    testcases = []
    for m in RE_TESTCASE.finditer(testcases_text):
        regs_before = tuple(map(int, m.group(1).split(', ')))  # type: Registers
        instruction = tuple(map(int, m.group(2).split(' ')))
        regs_after = tuple(map(int, m.group(3).split(', ')))  # type: Registers

        testcases.append(Testcase(
            registers_before=regs_before,
            instruction=Instruction(
                opcode=instruction[0],
                input_a=instruction[1],
                input_b=instruction[2],
                output=instruction[3]
            ),
            registers_after=regs_after,
        ))

    test_program = []
    for line in test_program_text.splitlines():
        instruction = tuple(map(int, line.split(' ')))
        test_program.append(Instruction(
            opcode=instruction[0],
            input_a=instruction[1],
            input_b=instruction[2],
            output=instruction[3]
        ))

    return testcases, test_program


class Cpu(object):
    __slots__ = ('registers', )

    def __init__(self):
        self.registers = [0, 0, 0, 0]

    def op_addr(self, a: int, b: int, c: int):
        self.registers[c] = self.registers[a] + self.registers[b]

    def op_addi(self, a: int, b: int, c: int):
        self.registers[c] = self.registers[a] + b

    def op_mulr(self, a: int, b: int, c: int):
        self.registers[c] = self.registers[a] * self.registers[b]

    def op_muli(self, a: int, b: int, c: int):
        self.registers[c] = self.registers[a] * b

    def op_banr(self, a: int, b: int, c: int):
        self.registers[c] = self.registers[a] & self.registers[b]

    def op_bani(self, a: int, b: int, c: int):
        self.registers[c] = self.registers[a] & b

    def op_borr(self, a: int, b: int, c: int):
        self.registers[c] = self.registers[a] | self.registers[b]

    def op_bori(self, a: int, b: int, c: int):
        self.registers[c] = self.registers[a] | b

    def op_setr(self, a: int, _: int, c: int):
        self.registers[c] = self.registers[a]

    def op_seti(self, a: int, _: int, c: int):
        self.registers[c] = a

    def op_gtir(self, a: int, b: int, c: int):
        self.registers[c] = 1 if a > self.registers[b] else 0

    def op_gtri(self, a: int, b: int, c: int):
        self.registers[c] = 1 if self.registers[a] > b else 0

    def op_gtrr(self, a: int, b: int, c: int):
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def op_eqir(self, a: int, b: int, c: int):
        self.registers[c] = 1 if a == self.registers[b] else 0

    def op_eqri(self, a: int, b: int, c: int):
        self.registers[c] = 1 if self.registers[a] == b else 0

    def op_eqrr(self, a: int, b: int, c: int):
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0

    @property
    def operations(self) -> Dict[str, Callable]:
        return {k.replace('op_', ''): getattr(self, k) for k in dir(self) if k.startswith('op_')}
