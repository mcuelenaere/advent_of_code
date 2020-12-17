def neighbours((int, int, int, int) coordinate, bint enable_fourth_dimension):
    cdef list coordinates = list()
    cdef int x, y, z, w, min_w, max_w
    for x in range(coordinate[0] - 1, coordinate[0] + 2):
        for y in range(coordinate[1] - 1, coordinate[1] + 2):
            for z in range(coordinate[2] - 1, coordinate[2] + 2):
                if enable_fourth_dimension:
                    min_w = coordinate[3] - 1
                    max_w = coordinate[3] + 2
                else:
                    min_w = coordinate[3]
                    max_w = coordinate[3] + 1

                for w in range(min_w, max_w):
                    if x == coordinate[0] and y == coordinate[1] and z == coordinate[2] and w == coordinate[3]:
                        continue
                    coordinates.append((x, y, z, w))
    return coordinates
