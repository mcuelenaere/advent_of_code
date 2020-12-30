import re

from collections import defaultdict
from typing import Dict, Set, Tuple


Coordinate = Tuple[int, int]
Tile = Set[Coordinate]

RE_TILE_ID = re.compile(r"^Tile (\d+):$")


def parse_tile(text: str) -> Tile:
    tile = set()
    for y, line in enumerate(text.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                tile.add((x, y))
    return tile


def parse_tiles(text: str) -> Dict[int, Tile]:
    tiles = {}
    tile_id = None
    tile_text = ""
    for line in text.splitlines():
        if line.startswith("Tile"):
            m = RE_TILE_ID.match(line)
            assert m is not None
            tile_id = int(m.group(1))
        elif line == "":
            tiles[tile_id] = parse_tile(tile_text)
            tile_text = ""
            tile_id = None
        else:
            tile_text += line + "\n"
    tiles[tile_id] = parse_tile(tile_text)

    return tiles


Graph = Dict[int, Dict[int, Tuple[int, int]]]


def match_tiles(tiles: Dict[int, Tile]) -> Graph:
    # extract borders
    borders_by_tile = {}
    for tile_id, tile in tiles.items():
        borders = [
            # north
            tuple(x for x in range(10) if (x, 0) in tile),
            # east
            tuple(y for y in range(10) if (9, y) in tile),
            # south
            tuple(x for x in range(10) if (x, 9) in tile),
            # west
            tuple(y for y in range(10) if (0, y) in tile),
        ]
        borders.extend(
            [
                # north, flipped horizontally
                tuple(sorted(9 - i for i in borders[0])),
                # east, flipped vertically
                tuple(sorted(9 - i for i in borders[1])),
                # south, flipped horizontally
                tuple(sorted(9 - i for i in borders[2])),
                # west, flipped vertically
                tuple(sorted(9 - i for i in borders[3])),
            ]
        )
        borders_by_tile[tile_id] = borders

    # build lookup table
    lookup = defaultdict(set)
    for tile_id, borders in borders_by_tile.items():
        for border in borders:
            lookup[border].add(tile_id)

    # match tiles
    graph = defaultdict(dict)
    for border, tile_ids in lookup.items():
        if len(tile_ids) < 2:
            continue

        assert len(tile_ids) == 2
        tile_a, tile_b = tile_ids
        graph[tile_a][tile_b] = (borders_by_tile[tile_a].index(border) % 4, borders_by_tile[tile_b].index(border) % 4)
        graph[tile_b][tile_a] = (borders_by_tile[tile_b].index(border) % 4, borders_by_tile[tile_a].index(border) % 4)

    return graph
