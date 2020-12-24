# distutils: language = c++

from cython.operator cimport dereference as deref
from libcpp.pair cimport pair
from libcpp.unordered_map cimport unordered_map
from libcpp.unordered_set cimport unordered_set
from libcpp.vector cimport vector

cdef extern from "coordinate.h" nogil:
    cdef cppclass Coordinate:
        int x, y
        Coordinate() except +
        Coordinate(int, int) except +
        bint operator==(Coordinate&, Coordinate&)
        Coordinate operator+(Coordinate&, Coordinate&)
    cdef cppclass CoordinateHasher:
        size_t operator()(Coordinate&)

cdef Coordinate[6] DIRECTIONS = [
    # e
    Coordinate(1, 0),
    # se
    Coordinate(0, 1),
    # sw
    Coordinate(-1, 1),
    # w
    Coordinate(-1, 0),
    # nw
    Coordinate(0, -1),
    # ne
    Coordinate(1, -1),
]

cdef unordered_map[Coordinate, bint, CoordinateHasher] _flip_tiles(unordered_map[Coordinate, bint, CoordinateHasher] tiles, int rounds) nogil:
    cdef vector[Coordinate] to_be_flipped
    cdef unordered_set[Coordinate, CoordinateHasher] outer_white_tiles
    cdef int black_neighbours
    cdef bint color
    cdef Coordinate neighbour, tile

    for _ in range(rounds):
        to_be_flipped.clear()
        outer_white_tiles.clear()

        for p in tiles:
            tile, color = p.first, p.second

            black_neighbours = 0
            for direction in DIRECTIONS:
                neighbour = tile + direction
                it = tiles.find(neighbour)
                if it != tiles.end():
                    if deref(it).second == True:
                        black_neighbours += 1
                else:
                    outer_white_tiles.insert(neighbour)

            if color and (black_neighbours == 0 or black_neighbours > 2):
                to_be_flipped.push_back(tile)
            elif not color and black_neighbours == 2:
                to_be_flipped.push_back(tile)

        for tile in outer_white_tiles:
            black_neighbours = 0
            for direction in DIRECTIONS:
                it = tiles.find(tile + direction)
                if it != tiles.end() and deref(it).second == True:
                    black_neighbours += 1

            if black_neighbours == 2:
                to_be_flipped.push_back(tile)

        for tile in to_be_flipped:
            it = tiles.find(tile)
            if it == tiles.end():
                tiles.insert(pair[Coordinate, bint](tile, True))
            else:
                p = deref(it)
                tiles[p.first] = p.second ^ True

    return tiles

def flip_tiles(dict tiles, int rounds):
    cdef unordered_map[Coordinate, bint, CoordinateHasher] _tiles
    for tile, color in tiles.items():
        _tiles.insert(
            pair[Coordinate, bint](Coordinate(tile[0], tile[1]), color)
        )

    _tiles = _flip_tiles(_tiles, rounds)

    tiles = {}
    for p in _tiles:
        tiles[(p.first.x, p.first.y)] = p.second

    return tiles
