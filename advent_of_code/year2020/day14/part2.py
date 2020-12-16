from .shared import Bitmask, MemoryWrite, parse_operations


def calculate(text: str) -> int:
    bitmask_set = 0
    floating_bits = ()
    memory = dict()
    for operation in parse_operations(text):
        if isinstance(operation, Bitmask):
            bitmask_set = sum(2 ** i for i, b in operation.bits if b == "1")
            floating_bits = tuple(i for i, b in operation.bits if b == "X")
        elif isinstance(operation, MemoryWrite):
            address = operation.address
            address |= bitmask_set
            for i in range(2 ** len(floating_bits)):
                for j in range(len(floating_bits)):
                    address &= ~(1 << floating_bits[j])
                    if i & (1 << j) != 0:
                        address |= 1 << floating_bits[j]
                memory[address] = operation.data
    return sum(memory.values())


puzzle = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
assert calculate(puzzle) == 208
