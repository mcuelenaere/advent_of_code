from .shared import Bitmask, MemoryWrite, parse_operations


def calculate(text: str) -> int:
    bitmask_clear = 0
    bitmask_set = 0
    memory = dict()
    for operation in parse_operations(text):
        if isinstance(operation, Bitmask):
            bitmask_set = sum(2**i for i, b in operation.bits if b == "1")
            bitmask_clear = sum(2**i for i, b in operation.bits if b == "0")
        elif isinstance(operation, MemoryWrite):
            memory[operation.address] = (operation.data & ~bitmask_clear) | bitmask_set
    return sum(memory.values())


puzzle = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
assert calculate(puzzle) == 165
