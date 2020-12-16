from .shared import parse_puzzle, Cpu


def calculate(puzzle: str) -> int:
    testcases, _ = parse_puzzle(puzzle)
    cpu = Cpu()
    samples_with_three_or_more_opcode_matches = 0
    for testcase in testcases:
        opcode_match_count = 0
        for op, fn in cpu.operations.items():
            cpu.registers = list(testcase.registers_before)
            fn(testcase.instruction.input_a, testcase.instruction.input_b, testcase.instruction.output)
            if tuple(cpu.registers) == testcase.registers_after:
                opcode_match_count += 1
        if opcode_match_count >= 3:
            samples_with_three_or_more_opcode_matches += 1
    return samples_with_three_or_more_opcode_matches
