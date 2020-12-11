from typing import Set, Tuple

Seat = Tuple[int, int]


def parse_map(text: str, search_character: str = 'L') -> Tuple[Set[Seat], Seat]:
    seats = set()
    max_x = 0
    for y, line in enumerate(text.splitlines()):
        for x, char in enumerate(line):
            if char == search_character:
                seats.add((x, y))
            max_x = max(x, max_x)
    return seats, (max_x, y)


DIRECTIONS = (
    # north
    (0, 1),
    # north-east
    (1, 1),
    # east
    (1, 0),
    # south-east
    (1, -1),
    # south
    (0, -1),
    # south-west
    (-1, -1),
    # west
    (-1, 0),
    # north-west
    (-1, 1),
)


def count_adjacent_seats(seat: Seat, available_seats: Set[Seat], occupied_seats: Set[Seat], max_position: Seat, enable_line_of_sight: bool):
    count = 0
    for d_x, d_y in DIRECTIONS:
        if enable_line_of_sight:
            i = 1
            while True:
                x = seat[0] + d_x * i
                y = seat[1] + d_y * i
                if x < 0 or y < 0:
                    break
                elif x > max_position[0] or y > max_position[1]:
                    break

                if (x, y) in available_seats:
                    # an available seat is blocking our view
                    break
                elif (x, y) in occupied_seats:
                    # found an occupied seat
                    count += 1
                    break

                i += 1
        else:
            x = seat[0] + d_x
            y = seat[1] + d_y
            count += 1 if (x, y) in occupied_seats else 0

    return count


def _test_count_adjacent_seats(text: str):
    seats, max_pos = parse_map(text, "L")
    occupied_seats, _ = parse_map(text, "#")
    start_seat = min(seats)
    return count_adjacent_seats(start_seat, seats, occupied_seats, max_pos, True)


assert _test_count_adjacent_seats(""".......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....""") == 8
assert _test_count_adjacent_seats(""".............
.L.L.#.#.#.#.
.............""") == 0
assert _test_count_adjacent_seats(""".##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.""") == 0


def find_stable_state(seats: Set[Seat], max_position: Seat, enable_line_of_sight: bool, required_seat_count: int) -> Tuple[Set[Seat], Set[Seat]]:
    available_seats = seats.copy()
    occupied_seats = set()

    while True:
        # perform a round
        old_available_seats = available_seats.copy()
        old_occupied_seats = occupied_seats.copy()
        for seat in seats:
            count = count_adjacent_seats(seat, old_available_seats, old_occupied_seats, max_position, enable_line_of_sight)
            if seat not in old_occupied_seats and count == 0:
                # seat becomes occupied
                occupied_seats.add(seat)
                available_seats.remove(seat)
            elif seat in old_occupied_seats and count >= required_seat_count:
                # seat becomes available
                occupied_seats.remove(seat)
                available_seats.add(seat)

        if len(occupied_seats) == len(old_occupied_seats):
            # we reached a stable state
            break

    return available_seats, occupied_seats
