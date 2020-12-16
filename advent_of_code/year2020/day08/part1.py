from .shared import Cpu, parse_instructions


def calculate(text: str) -> int:
    cpu = Cpu(instructions=list(parse_instructions(text)))
    seen_ips = set()
    while cpu.instruction_pointer not in seen_ips:
        seen_ips.add(cpu.instruction_pointer)
        cpu.step()
    return cpu.accumulator


puzzle = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
assert calculate(puzzle) == 5
