from .shared import parse_instructions, MusicProcessingUnit


def calculate(text: str) -> int:
    instructions = tuple(parse_instructions(text))
    mpu = MusicProcessingUnit(instructions)

    mpu.execute_step()
    while mpu.recovered_frequency is None:
        mpu.execute_step()
    return mpu.recovered_frequency


puzzle = """
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
""".strip()
assert calculate(puzzle) == 4
