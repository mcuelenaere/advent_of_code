from collections import defaultdict
from typing import Dict

from .shared import Coordinate, adjacent_tiles, move, parse_paths


try:
    from .part2_native import flip_tiles
except ImportError:

    def flip_tiles(tiles: Dict[Coordinate, bool], rounds: int) -> Dict[Coordinate, bool]:
        for day in range(rounds):
            to_be_flipped = []
            outer_white_tiles = set()
            for tile, color in tiles.items():
                black_neighbours = 0
                for neighbour in adjacent_tiles(tile):
                    if neighbour in tiles:
                        if tiles[neighbour]:
                            black_neighbours += 1
                    else:
                        outer_white_tiles.add(neighbour)

                if color and (black_neighbours == 0 or black_neighbours > 2):
                    to_be_flipped.append(tile)
                elif not color and black_neighbours == 2:
                    to_be_flipped.append(tile)

            for tile in outer_white_tiles:
                black_neighbours = sum(
                    1 for neighbour in adjacent_tiles(tile) if neighbour in tiles and tiles[neighbour]
                )
                if black_neighbours == 2:
                    to_be_flipped.append(tile)

            for tile in to_be_flipped:
                if tile in tiles:
                    tiles[tile] ^= True
                else:
                    tiles[tile] = True

        return tiles


def calculate(text: str) -> int:
    paths = tuple(parse_paths(text))

    # initial pattern
    tiles = defaultdict(bool)
    for path in paths:
        pos = move((0, 0), path)
        tiles[pos] ^= True

    # flip tiles for 100 days
    tiles = flip_tiles(dict(tiles), 100)

    return sum(1 for v in tiles.values() if v)


puzzle = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""
assert calculate(puzzle) == 2208
