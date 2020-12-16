cdef char[16] DIRECTIONS = [
    # north
    0, 1,
    # north-east
    1, 1,
    # east
    1, 0,
    # south-east
    1, -1,
    # south
    0, -1,
    # south-west
    -1, -1,
    # west
    -1, 0,
    # north-west
    -1, 1,
]

def count_adjacent_seats(
    (int, int) seat,
    set available_seats,
    set occupied_seats,
    (int, int) max_position,
    bint enable_line_of_sight,
):
    cdef unsigned int count = 0
    cdef char d_x, d_y
    cdef int x, y
    cdef unsigned int i, j

    for j in range(0, 16, 2):
        d_x = DIRECTIONS[j]
        d_y = DIRECTIONS[j + 1]

        if enable_line_of_sight:
            i = 1
            while True:
                x = seat[0] + d_x * i
                y = seat[1] + d_y * i
                if x < 0 or y < 0:
                    break
                elif x > max_position[0] or y > max_position[1]:
                    break

                seat_to_check = (x, y)
                if seat_to_check in available_seats:
                    # an available seat is blocking our view
                    break
                elif seat_to_check in occupied_seats:
                    # found an occupied seat
                    count += 1
                    break

                i += 1
        else:
            x = seat[0] + d_x
            y = seat[1] + d_y
            count += 1 if (x, y) in occupied_seats else 0

    return count
