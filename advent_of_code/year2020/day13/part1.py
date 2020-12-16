from .shared import parse_schedule


def calculate(text: str) -> int:
    estimate, bus_lines = parse_schedule(text)
    line, wait_time = min(
        ((line, line - (estimate % line)) for line in bus_lines if line is not None),
        key=lambda x: x[1],
    )
    return line * wait_time


puzzle = """939
7,13,x,x,59,x,31,19"""
assert calculate(puzzle) == 295
