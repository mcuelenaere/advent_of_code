from .shared import find_stable_state, parse_map


def calculate(text: str) -> int:
    seats, max_pos = parse_map(text)
    _, occupied_seats = find_stable_state(seats, max_pos, enable_line_of_sight=True, required_seat_count=5)
    return len(occupied_seats)


puzzle = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
assert calculate(puzzle) == 26
