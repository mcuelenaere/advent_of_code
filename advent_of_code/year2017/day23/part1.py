from .shared import Coprocessor, IMul, parse_instructions


def calculate(text: str) -> int:
    instructions = tuple(parse_instructions(text))
    cpu = Coprocessor(instructions)

    number_of_muls = 0
    while cpu.instruction_offset < len(cpu.instructions):
        if isinstance(cpu.instructions[cpu.instruction_offset], IMul):
            number_of_muls += 1
        cpu.execute_step()
    return number_of_muls
