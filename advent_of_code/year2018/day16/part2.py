from .shared import parse_puzzle, Cpu


def calculate(puzzle: str) -> int:
    testcases, test_program = parse_puzzle(puzzle)

    # figure out meaning of opcodes
    opcode_mapping = {}
    cpu = Cpu()
    for testcase in testcases:
        potential_matches = set()
        for op, fn in cpu.operations.items():
            cpu.registers = list(testcase.registers_before)
            fn(testcase.instruction.input_a, testcase.instruction.input_b, testcase.instruction.output)
            if tuple(cpu.registers) == testcase.registers_after:
                potential_matches.add(op)

        if testcase.instruction.opcode not in opcode_mapping:
            opcode_mapping[testcase.instruction.opcode] = potential_matches
        else:
            opcode_mapping[testcase.instruction.opcode] &= potential_matches

    # now reduce opcode_mapping
    for _ in range(15):
        single_opcodes = {tuple(v)[0] for v in opcode_mapping.values() if len(v) == 1}
        opcode_mapping = {k: (v - single_opcodes if len(v) != 1 else v) for k, v in opcode_mapping.items()}

    # get rid of sets
    opcode_mapping = {k: tuple(v)[0] for k, v in opcode_mapping.items()}

    # execute test program
    cpu = Cpu()
    ops = cpu.operations
    for instruction in test_program:
        fn = ops[opcode_mapping[instruction.opcode]]
        fn(instruction.input_a, instruction.input_b, instruction.output)
    return cpu.registers[0]
