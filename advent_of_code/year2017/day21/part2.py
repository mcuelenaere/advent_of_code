from .shared import parse_pattern_book, parse_pattern, process_pattern, count_enabled


def calculate(text: str) -> int:
    start_pattern = parse_pattern(".#./..#/###")
    pattern_book = parse_pattern_book(text)

    pattern = start_pattern
    for _ in range(18):
        pattern = process_pattern(pattern, pattern_book)

    return count_enabled(pattern)
