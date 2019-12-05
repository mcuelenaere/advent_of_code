
from math import floor, inf
from typing import List

Instructions = List[int]


OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_READ_INPUT = 3
OPCODE_WRITE_OUTPUT = 4
OPCODE_JUMP_IF_TRUE = 5
OPCODE_JUMP_IF_FALSE = 6
OPCODE_LESS_THAN = 7
OPCODE_EQUALS = 8
OPCODE_EXIT = 99


def evaluate(instructions: Instructions, input: int) -> int:
    index = 0
    output = -inf  # default the output to an invalid value
    while True:
        # fetch current opcode
        instruction = instructions[index]

        param1_is_immediate = floor((instruction / 1e2) % 10) == 1
        param2_is_immediate = floor((instruction / 1e3) % 10) == 1
        param3_is_immediate = floor((instruction / 1e4) % 10) == 1
        opcode = instruction % 100

        if opcode == OPCODE_ADD:
            val_a = instructions[index + 1]
            if not param1_is_immediate:
                val_a = instructions[val_a]
            val_b = instructions[index + 2]
            if not param2_is_immediate:
                val_b = instructions[val_b]
            addr_out = instructions[index + 3]
            assert not param3_is_immediate
            instructions[addr_out] = val_a + val_b
            index += 4
        elif opcode == OPCODE_MULTIPLY:
            val_a = instructions[index + 1]
            if not param1_is_immediate:
                val_a = instructions[val_a]
            val_b = instructions[index + 2]
            if not param2_is_immediate:
                val_b = instructions[val_b]
            addr_out = instructions[index + 3]
            assert not param3_is_immediate
            instructions[addr_out] = val_a * val_b
            index += 4
        elif opcode == OPCODE_READ_INPUT:
            addr = instructions[index + 1]
            instructions[addr] = input
            index += 2
        elif opcode == OPCODE_WRITE_OUTPUT:
            val_a = instructions[index + 1]
            if not param1_is_immediate:
                val_a = instructions[val_a]
            output = val_a
            index += 2
        elif opcode == OPCODE_JUMP_IF_TRUE:
            val_a = instructions[index + 1]
            if not param1_is_immediate:
                val_a = instructions[val_a]
            val_b = instructions[index + 2]
            if not param2_is_immediate:
                val_b = instructions[val_b]
            if val_a != 0:
                index = val_b
            else:
                # skip jump
                index += 3
        elif opcode == OPCODE_JUMP_IF_FALSE:
            val_a = instructions[index + 1]
            if not param1_is_immediate:
                val_a = instructions[val_a]
            val_b = instructions[index + 2]
            if not param2_is_immediate:
                val_b = instructions[val_b]
            if val_a == 0:
                index = val_b
            else:
                # skip jump
                index += 3
        elif opcode == OPCODE_LESS_THAN:
            val_a = instructions[index + 1]
            if not param1_is_immediate:
                val_a = instructions[val_a]
            val_b = instructions[index + 2]
            if not param2_is_immediate:
                val_b = instructions[val_b]
            addr_out = instructions[index + 3]
            assert not param3_is_immediate
            instructions[addr_out] = 1 if val_a < val_b else 0
            index += 4
        elif opcode == OPCODE_EQUALS:
            val_a = instructions[index + 1]
            if not param1_is_immediate:
                val_a = instructions[val_a]
            val_b = instructions[index + 2]
            if not param2_is_immediate:
                val_b = instructions[val_b]
            addr_out = instructions[index + 3]
            assert not param3_is_immediate
            instructions[addr_out] = 1 if val_a == val_b else 0
            index += 4
        elif opcode == OPCODE_EXIT:
            # evaluation ended
            return output
        else:
            raise RuntimeError(f"Invalid opcode {opcode} at index {index}")


def _test_eval_simple(text: str) -> str:
    instructions = list(map(int, text.strip().split(',')))
    evaluate(instructions, 0)
    return ",".join(map(str, instructions))


def _test_eval_with_io(text: str, input: int) -> int:
    instructions = list(map(int, text.strip().split(',')))
    return evaluate(instructions, input)


assert _test_eval_simple("1101,100,-1,4,0") == "1101,100,-1,4,99"
assert _test_eval_with_io("3,9,8,9,10,9,4,9,99,-1,8", 8) == 1
assert _test_eval_with_io("3,9,8,9,10,9,4,9,99,-1,8", 5) == 0
assert _test_eval_with_io("3,9,7,9,10,9,4,9,99,-1,8", 8) == 0
assert _test_eval_with_io("3,9,7,9,10,9,4,9,99,-1,8", 5) == 1
assert _test_eval_with_io("3,3,1108,-1,8,3,4,3,99", 8) == 1
assert _test_eval_with_io("3,3,1108,-1,8,3,4,3,99", 5) == 0
assert _test_eval_with_io("3,3,1107,-1,8,3,4,3,99", 8) == 0
assert _test_eval_with_io("3,3,1107,-1,8,3,4,3,99", 5) == 1
assert _test_eval_with_io("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", 0) == 0
assert _test_eval_with_io("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", 5) == 1
assert _test_eval_with_io("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", 0) == 0
assert _test_eval_with_io("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", 5) == 1
assert _test_eval_with_io("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", 5) == 999
assert _test_eval_with_io("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", 8) == 1000
assert _test_eval_with_io("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", 13) == 1001
