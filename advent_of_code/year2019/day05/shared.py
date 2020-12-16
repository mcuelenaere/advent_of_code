from collections import defaultdict
from math import floor
from typing import List, Generator, Tuple

Instructions = List[int]


OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_READ_INPUT = 3
OPCODE_WRITE_OUTPUT = 4
OPCODE_JUMP_IF_TRUE = 5
OPCODE_JUMP_IF_FALSE = 6
OPCODE_LESS_THAN = 7
OPCODE_EQUALS = 8
OPCODE_ADJUST_RELATIVE_BASE = 9
OPCODE_EXIT = 99

MODE_POSITION = 0
MODE_IMMEDIATE = 1
MODE_RELATIVE = 2


def parse_instructions(text: str) -> Instructions:
    return list(map(int, text.strip().split(',')))


def streaming_evaluate(instructions: Instructions) -> Generator[int, int, None]:
    memory = defaultdict(int)
    memory.update(dict(enumerate(instructions)))

    index = 0
    relative_base = 0
    while True:
        # fetch current opcode
        instruction = memory[index]

        param_modes = [
            floor((instruction / 1e2) % 10),
            floor((instruction / 1e3) % 10),
            floor((instruction / 1e4) % 10),
        ]
        opcode = instruction % 100

        def parse_param(number: int) -> int:
            assert 0 < number < 4
            mode = param_modes[number - 1]
            assert 0 <= mode <= 2
            val = memory[index + number]
            if mode == MODE_POSITION:
                val = memory[val]
            elif mode == MODE_RELATIVE:
                val = memory[relative_base + val]
            return val

        def parse_addr(number: int) -> int:
            assert 0 < number < 4
            mode = param_modes[number - 1]
            assert 0 <= mode <= 2
            val = memory[index + number]
            if mode == MODE_RELATIVE:
                val += relative_base
            return val

        if opcode == OPCODE_ADD:
            val_a = parse_param(1)
            val_b = parse_param(2)
            addr_out = parse_addr(3)
            memory[addr_out] = val_a + val_b
            index += 4
        elif opcode == OPCODE_MULTIPLY:
            val_a = parse_param(1)
            val_b = parse_param(2)
            addr_out = parse_addr(3)
            memory[addr_out] = val_a * val_b
            index += 4
        elif opcode == OPCODE_READ_INPUT:
            addr = parse_addr(1)
            memory[addr] = yield
            assert isinstance(memory[addr], int), f"Expected int, got {memory[addr]}"
            index += 2
        elif opcode == OPCODE_WRITE_OUTPUT:
            val_a = parse_param(1)
            yield val_a
            index += 2
        elif opcode == OPCODE_JUMP_IF_TRUE:
            val_a = parse_param(1)
            val_b = parse_param(2)
            if val_a != 0:
                index = val_b
            else:
                # skip jump
                index += 3
        elif opcode == OPCODE_JUMP_IF_FALSE:
            val_a = parse_param(1)
            val_b = parse_param(2)
            if val_a == 0:
                index = val_b
            else:
                # skip jump
                index += 3
        elif opcode == OPCODE_LESS_THAN:
            val_a = parse_param(1)
            val_b = parse_param(2)
            addr_out = parse_addr(3)
            memory[addr_out] = 1 if val_a < val_b else 0
            index += 4
        elif opcode == OPCODE_EQUALS:
            val_a = parse_param(1)
            val_b = parse_param(2)
            addr_out = parse_addr(3)
            memory[addr_out] = 1 if val_a == val_b else 0
            index += 4
        elif opcode == OPCODE_ADJUST_RELATIVE_BASE:
            relative_base += parse_param(1)
            index += 2
        elif opcode == OPCODE_EXIT:
            # evaluation ended, write back instructions from memory
            for i in range(len(instructions)):
                instructions[i] = memory[i]
            return
        else:
            raise RuntimeError(f"Invalid opcode {opcode} at index {index}")


def evaluate(instructions: Instructions, input: int) -> int:
    last_output = -1  # default the output to an invalid value

    # initialize generator
    gen = streaming_evaluate(instructions)
    try:
        next(gen)
    except StopIteration:
        return last_output

    while True:
        try:
            # keep sending the same input over and over
            ret = gen.send(input)
            if isinstance(ret, int):
                # output instruction
                last_output = ret
        except StopIteration:
            break

    return last_output


def _test_eval_simple(text: str) -> str:
    instructions = parse_instructions(text)
    evaluate(instructions, 0)
    return ",".join(map(str, instructions))


def _test_eval_with_io(text: str, input: int) -> int:
    instructions = parse_instructions(text)
    return evaluate(instructions, input)


def _test_eval_with_multi_out(text: str) -> Tuple[int]:
    instructions = parse_instructions(text)
    outputs = tuple(streaming_evaluate(instructions))
    return outputs


# day 5 tests
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

# day 9 tests
assert _test_eval_with_multi_out("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99") == (109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16 ,101 ,1006 ,101 ,0 ,99)
assert _test_eval_with_multi_out("1102,34915192,34915192,7,4,7,99,0") == (1219070632396864,)
assert _test_eval_with_multi_out("104,1125899906842624,99") == (1125899906842624,)
