from .shared import parse_instructions, Processor


def calculate(text: str) -> int:
    instructions = tuple(parse_instructions(text))
    cpu = Processor(instructions)
    cpu.registers['a'] = 1
    while cpu.instruction_offset < len(cpu.instructions):
        cpu.execute_step()
    return cpu.registers['b']
