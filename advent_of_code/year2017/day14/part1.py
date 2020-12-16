from .shared import calculate_rows


def calculate(text: str) -> int:
    count = 0
    for row in calculate_rows(text):
        # count number of set bits
        count += bin(row).count('1')
    return count


assert calculate('flqrgnkx') == 8108
