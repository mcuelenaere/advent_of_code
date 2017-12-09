from .shared import Cpu, parse_instructions


def calculate(text: str) -> int:
    cpu = Cpu()
    instructions = parse_instructions(text.splitlines())
    max_value = 0
    for instruction in instructions:
        cpu.execute_instruction(instruction)
        max_value = max(max_value, *cpu.registers.values())
    return max_value


puzzle = """
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
""".strip()
assert calculate(puzzle) == 10
