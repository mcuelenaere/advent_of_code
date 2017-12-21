from .shared import parse_pattern_book, parse_pattern, process_pattern, count_enabled


def calculate(text: str, iteration_count=5) -> int:
    start_pattern = parse_pattern(".#./..#/###")
    pattern_book = parse_pattern_book(text)

    pattern = start_pattern
    for _ in range(iteration_count):
        pattern = process_pattern(pattern, pattern_book)

    return count_enabled(pattern)


puzzle = """
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
""".strip()
assert calculate(puzzle, 2) == 12
