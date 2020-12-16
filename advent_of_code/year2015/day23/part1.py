from .shared import Processor, parse_instructions


def calculate(text: str) -> int:
    instructions = tuple(parse_instructions(text))
    cpu = Processor(instructions)
    while cpu.instruction_offset < len(cpu.instructions):
        cpu.execute_step()
    return cpu.registers["b"]
