from collections import deque
from itertools import product
from math import sqrt
from typing import Dict, Optional, Tuple

from .shared import Graph, Tile, match_tiles, parse_tile, parse_tiles


def orient_tile(tile: Tile, size: int, rotation: int, hflip: bool, vflip: bool) -> Tile:
    size -= 1

    if hflip:
        tile = ((size - x, y) for x, y in tile)

    if vflip:
        tile = ((x, size - y) for x, y in tile)

    if rotation == 0:
        # do nothing
        pass
    elif rotation == 1:
        tile = ((size - y, x) for x, y in tile)
    elif rotation == 2:
        tile = ((size - x, size - y) for x, y in tile)
    elif rotation == 3:
        tile = ((y, size - x) for x, y in tile)

    return set(tile)


def shortest_path(graph: Graph, start: int, end: int) -> Optional[Tuple[int, ...]]:
    # dijkstra algorithm
    visited = {start: 0}
    path = {}
    nodes = {start}

    while len(nodes) > 0:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node == end:
            break
        elif min_node is None:
            return None

        nodes.remove(min_node)
        current_weight = visited[min_node]
        for edge in graph[min_node].keys():
            if edge not in visited:
                nodes.add(edge)

            weight = current_weight + 1
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    stack = deque()
    u = end
    while u is not None:
        stack.appendleft(u)
        u = path.get(u, None)

    if len(stack) == 1 and start != end:
        return None

    return tuple(stack)


def build_image(tiles: Dict[int, Tile], graph: Graph) -> Tuple[Tile, int]:
    dimension = int(sqrt(len(tiles)))
    corner_tiles = [tile_id for tile_id, links in graph.items() if len(links) == 2]

    # pick a certain set of corner tiles
    top_left_corner = corner_tiles[0]
    bottom_right_corner = next(
        tile for tile in corner_tiles if len(shortest_path(graph, top_left_corner, tile)) == dimension * 2 - 1
    )
    top_right_corner, bottom_left_corner = tuple(
        tile for tile in corner_tiles if tile not in (top_left_corner, bottom_right_corner)
    )
    left_path = shortest_path(graph, top_left_corner, bottom_left_corner)
    right_path = shortest_path(graph, top_right_corner, bottom_right_corner)

    # build the whole puzzle matrix
    puzzle = dict()
    for y, (left, right) in enumerate(zip(left_path, right_path)):
        for x, tile_id in enumerate(shortest_path(graph, left, right)):
            puzzle[(x, y)] = tile_id

    # build image
    image = set()
    for tile_y in range(dimension):
        for tile_x in range(dimension):
            tile_id = puzzle[(tile_x, tile_y)]

            neighbours = [
                # north
                ((tile_x, tile_y - 1), 0),
                # east
                ((tile_x + 1, tile_y), 1),
                # south
                ((tile_x, tile_y + 1), 2),
                # west
                ((tile_x - 1, tile_y), 3),
            ]

            def is_valid(rotation: int, hflip: int, vflip: int) -> bool:
                for neighbour, expected_direction in neighbours:
                    if neighbour not in puzzle:
                        continue

                    neighbour_tile_id = puzzle[neighbour]
                    my_direction, _ = graph[tile_id][neighbour_tile_id]
                    if hflip and my_direction in (1, 3):
                        my_direction = (my_direction + 2) % 4
                    if vflip and my_direction in (0, 2):
                        my_direction = (my_direction + 2) % 4
                    my_direction = (my_direction + rotation) % 4
                    if my_direction != expected_direction:
                        return False

                return True

            # bruteforce all possible combinations
            rotation, hflip, vflip = next(
                args for args in product((0, 1, 2, 3), (True, False), (True, False)) if is_valid(*args)
            )

            # orient tile correctly
            tile = orient_tile(tiles[tile_id], 10, rotation, hflip, vflip)

            # remove boundaries
            tile = set((x - 1, y - 1) for x, y in tile if 0 < x < 9 and 0 < y < 9)

            # update image
            image.update((x + tile_x * 8, y + tile_y * 8) for x, y in tile)

    return image, dimension * 8


MONSTER = parse_tile(
    """
                  #
#    ##    ##    ###
 #  #  #  #  #  #
""".strip(
        "\n"
    )
)
MONSTER_WIDTH = max(x for x, y in MONSTER) + 1
MONSTER_HEIGHT = max(y for x, y in MONSTER) + 1


def calculate(text: str) -> int:
    tiles = parse_tiles(text)
    graph = match_tiles(tiles)
    image, image_size = build_image(tiles, graph)

    # pre-calculate list of offsetted monsters
    offsetted_monsters = []
    for x_offset in range(image_size - MONSTER_WIDTH):
        for y_offset in range(image_size - MONSTER_HEIGHT):
            offsetted_monsters.append({(x + x_offset, y + y_offset) for x, y in MONSTER})

    # find monsters
    max_roughness = float("inf")
    for rotation, hflip, vflip in product((0, 1, 2, 3), (True, False), (True, False)):
        if hflip and vflip:
            # this is the same as rotating 180 degrees
            continue

        # orient image correctly
        oriented_image = orient_tile(image, image_size, rotation, hflip, vflip)

        # count number of monsters
        monster_count = sum(
            1 if offsetted_monster.issubset(oriented_image) else 0 for offsetted_monster in offsetted_monsters
        )

        # update max roughness
        roughness = len(image) - len(MONSTER) * monster_count
        max_roughness = min(max_roughness, roughness)

    return max_roughness


puzzle = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""
assert calculate(puzzle) == 273
