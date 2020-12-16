from .shared import count_enabled, parse_pattern, parse_pattern_book, process_pattern


def calculate(text: str) -> int:
    start_pattern = parse_pattern(".#./..#/###")
    pattern_book = parse_pattern_book(text)

    pattern = start_pattern
    for _ in range(18):
        pattern = process_pattern(pattern, pattern_book)

    return count_enabled(pattern)
