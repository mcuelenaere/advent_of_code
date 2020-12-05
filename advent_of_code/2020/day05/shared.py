import math


def decode_seat_id(text: str) -> int:
    assert len(text) == 10

    min_row = 0
    max_row = 127
    for char in text[:7]:
        if char == 'F':
            max_row = math.floor((min_row + max_row) / 2)
        elif char == 'B':
            min_row = math.ceil((min_row + max_row) / 2)
        else:
            raise AssertionError("Expected F or B")
    assert min_row == max_row

    min_column = 0
    max_column = 7
    for char in text[7:10]:
        if char == 'L':
            max_column = math.floor((min_column + max_column) / 2)
        elif char == 'R':
            min_column = math.ceil((min_column + max_column) / 2)
        else:
            raise AssertionError("Expected R or L")
    assert min_column == max_column

    row = min_row
    column = min_column
    seat_id = row * 8 + column
    return seat_id


assert decode_seat_id("FBFBBFFRLR") == 357
assert decode_seat_id("BFFFBBFRRR") == 567
assert decode_seat_id("FFFBBBFRRR") == 119
assert decode_seat_id("BBFFBBFRLL") == 820
