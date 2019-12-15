from ..day05.shared import streaming_evaluate, parse_instructions
from collections import deque
from typing import Tuple, Set

STATUS_HIT_WALL = 0
STATUS_MOVED_STEP = 1
STATUS_FOUND_OXYGEN = 2

MOVE_NORTH = 1
MOVE_SOUTH = 2
MOVE_WEST = 3
MOVE_EAST = 4

MOVEMENT_VECTORS = (
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
)

Position = Tuple[int, int]


def discover_map(text: str) -> Tuple[Set[Position], Position]:
    instructions = parse_instructions(text)
    gen = streaming_evaluate(instructions)

    walls = set()
    visited_path = deque(((0, 0),))
    visited_places = {(0, 0)}
    x = 0
    y = 0
    direction = None
    oxygen_location = None
    while True:
        try:
            res = next(gen)
            if res is None:
                # move to next position
                for i in range(1, 5):
                    new_x = x + MOVEMENT_VECTORS[i - 1][0]
                    new_y = y + MOVEMENT_VECTORS[i - 1][1]
                    if (new_x, new_y) in walls:
                        continue
                    elif (new_x, new_y) in visited_places:
                        continue

                    direction = i
                    break
                else:
                    #  we have to backtrack
                    if len(visited_path) == 1:
                        # nothing to do anymore
                        break
                    visited_path.pop()
                    old_x, old_y = visited_path.pop()
                    direction = MOVEMENT_VECTORS.index((old_x - x, old_y - y)) + 1

                status = gen.send(direction)
            else:
                status = res

            if status == STATUS_HIT_WALL:
                wall_x = x + MOVEMENT_VECTORS[direction - 1][0]
                wall_y = y + MOVEMENT_VECTORS[direction - 1][1]
                walls.add((wall_x, wall_y))
            elif status == STATUS_MOVED_STEP:
                x += MOVEMENT_VECTORS[direction - 1][0]
                y += MOVEMENT_VECTORS[direction - 1][1]
                visited_places.add((x, y))
                visited_path.append((x, y))
            elif status == STATUS_FOUND_OXYGEN:
                x += MOVEMENT_VECTORS[direction - 1][0]
                y += MOVEMENT_VECTORS[direction - 1][1]
                oxygen_location = (x, y)
                visited_places.add((x, y))
                visited_path.append((x, y))
            else:
                raise RuntimeError(f'unknown statuscode {status}')
        except StopIteration:
            break

    return walls, oxygen_location


def adjacent_positions(position: Position) -> Tuple[Position, ...]:
    x, y = position
    return (
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
    )


def manhattan_distance(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def shortest_path(start: Position, end: Position, walls: Set[Position]) -> Tuple[Position, ...]:
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
            raise RuntimeError('no path found')

        nodes.remove(min_node)
        current_weight = visited[min_node]
        for edge in adjacent_positions(min_node):
            if edge in walls:
                continue

            if edge not in visited:
                nodes.add(edge)

            weight = current_weight + manhattan_distance(min_node, edge)
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    stack = deque()
    u = end
    while u is not None:
        stack.appendleft(u)
        u = path.get(u, None)

    return tuple(stack)


def flood_region(walls: Set[Position], start: Position):
    # do BFS
    filled_tiles = set()
    stack = deque()
    stack.append([start])

    iterations = 0
    while len(stack) > 0:
        next_positions = []
        for pos in stack.pop():
            for point in adjacent_positions(pos):
                if point in walls or point in filled_tiles:
                    continue

                filled_tiles.add(point)
                next_positions.append(point)

        if len(next_positions) > 0:
            stack.append(next_positions)
            iterations += 1

    return iterations


_ = {(1, 0), (2, 0), (0, 1), (3, 1), (4, 1), (0, 2), (2, 2), (5, 2), (0, 3), (4, 3), (1, 4), (2, 4), (3, 4)}
assert flood_region(_, (2, 3)) == 4
