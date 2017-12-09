from .shared import Cpu, parse_instructions


def calculate(text: str) -> int:
    cpu = Cpu()
    instructions = parse_instructions(text.splitlines())
    for instruction in instructions:
        cpu.execute_instruction(instruction)
    return max(cpu.registers.values())


puzzle = """
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
""".strip()
assert calculate(puzzle) == 1
