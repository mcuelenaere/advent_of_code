from .shared import evaluate


def calculate(text: str) -> int:
    for noun in range(0, 100):
        for verb in range(0, 100):
            opcodes = list(map(int, text.strip().split(',')))
            opcodes[1] = noun
            opcodes[2] = verb
            evaluate(opcodes)
            if opcodes[0] == 19690720:
                return 100 * noun + verb
