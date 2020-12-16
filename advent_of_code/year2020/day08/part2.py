from typing import Optional

from .shared import Cpu, Instruction, Instructions, InstructionType, parse_instructions


def test_program(instructions: Instructions) -> Optional[int]:
    cpu = Cpu(instructions)
    seen_ips = set()
    while cpu.instruction_pointer < len(cpu.instructions) and cpu.instruction_pointer not in seen_ips:
        seen_ips.add(cpu.instruction_pointer)
        cpu.step()

    if cpu.instruction_pointer >= len(cpu.instructions):
        # found the correct patch
        return cpu.accumulator
    else:
        # infinite loop
        return None


def calculate(text: str) -> int:
    instructions = tuple(parse_instructions(text))
    for idx, instruction in enumerate(instructions):
        if instruction.type == InstructionType.NOP and instruction.offset != 0:
            new_instruction = Instruction(InstructionType.JMP, instruction.offset)
        elif instruction.type == InstructionType.JMP:
            new_instruction = Instruction(InstructionType.NOP, instruction.offset)
        else:
            continue

        result = test_program(instructions[:idx] + (new_instruction,) + instructions[idx + 1 :])
        if result is not None:
            return result

    raise RuntimeError("did not find patch")


puzzle = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
assert calculate(puzzle) == 8
