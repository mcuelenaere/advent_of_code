from typing import List


Opcodes = List[int]


def evaluate(opcodes: Opcodes):
    index = 0
    while True:
        # fetch current opcode
        opcode = opcodes[index]
        if opcode == 1:
            addr_in_a = opcodes[index + 1]
            addr_in_b = opcodes[index + 2]
            addr_out = opcodes[index + 3]
            opcodes[addr_out] = opcodes[addr_in_a] + opcodes[addr_in_b]
            index += 4
        elif opcode == 2:
            addr_in_a = opcodes[index + 1]
            addr_in_b = opcodes[index + 2]
            addr_out = opcodes[index + 3]
            opcodes[addr_out] = opcodes[addr_in_a] * opcodes[addr_in_b]
            index += 4
        elif opcode == 99:
            # evaluation ended
            return
        else:
            raise RuntimeError(f"Invalid opcode {opcode} at index {index}")


def _test_eval(text: str) -> str:
    opcodes = list(map(int, text.strip().split(",")))
    evaluate(opcodes)
    return ",".join(map(str, opcodes))


assert _test_eval("1,9,10,3,2,3,11,0,99,30,40,50") == "3500,9,10,70,2,3,11,0,99,30,40,50"
assert _test_eval("1,0,0,0,99") == "2,0,0,0,99"
assert _test_eval("2,3,0,3,99") == "2,3,0,6,99"
assert _test_eval("2,4,4,5,99,0") == "2,4,4,5,99,9801"
assert _test_eval("1,1,1,4,99,5,6,0,99") == "30,1,1,4,2,5,6,0,99"
