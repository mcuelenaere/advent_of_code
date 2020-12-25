try:
    from .part1_native import determine_loop_size
except ImportError:

    def determine_loop_size(expected_outcome: int) -> int:
        value = 1
        loop_size = 0
        while True:
            value *= 7
            value %= 20201227
            loop_size += 1
            if value == expected_outcome:
                return loop_size


assert determine_loop_size(5764801) == 8
assert determine_loop_size(17807724) == 11


try:
    from .part1_native import transform
except ImportError:

    def transform(subject_number: int, loop_size: int) -> int:
        value = 1
        for _ in range(loop_size):
            value *= subject_number
            value %= 20201227
        return value


assert transform(7, 8) == 5764801
assert transform(7, 11) == 17807724
assert transform(17807724, 8) == 14897079
assert transform(5764801, 11) == 14897079


def calculate(text: str) -> int:
    a_key, b_key = map(int, text.splitlines())
    a_loop_size = determine_loop_size(a_key)
    return transform(b_key, a_loop_size)


puzzle = """5764801
17807724"""
assert calculate(puzzle) == 14897079
