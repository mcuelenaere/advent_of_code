from collections import deque
from enum import Enum
from typing import Set, NamedTuple, Tuple, Iterable, Optional

Position = Tuple[int, int]


class CharacterType(Enum):
    Elf = 'Elf'
    Goblin = 'Goblin'

    @property
    def opponent(self):
        return CharacterType.Goblin if self == CharacterType.Elf else CharacterType.Elf


def adjacent_positions(position: Position) -> Tuple[Position, ...]:
    x, y = position
    return (
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
    )


class Character(NamedTuple):
    type: CharacterType
    attack_power: int
    hit_points: int
    position: Position

    def adjacent_positions(self) -> Tuple[Position, ...]:
        return adjacent_positions(self.position)

    def __str__(self):
        if self.type == CharacterType.Elf:
            return 'E'
        elif self.type == CharacterType.Goblin:
            return 'G'


class State(NamedTuple):
    walls: Set[Position]
    characters: Tuple[Character, ...]

    def tiles(self):
        d = {}
        d.update((pos, '#') for pos in self.walls)
        d.update((char.position, str(char)) for char in self.characters)
        return d

    def __str__(self):
        tiles = self.tiles()
        max_x = max(x for x, _ in tiles.keys())
        max_y = max(y for _, y in tiles.keys())
        lines = []
        for y in range(max_y + 1):
            lines.append(''.join(tiles.get((x, y), '.') for x in range(max_x + 1)))
        return '\n'.join(lines)


def parse_state(text: str, elf_attack_power: int = 3, goblin_attack_power: int = 3) -> State:
    walls = set()
    characters = list()
    for y, line in enumerate(text.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                walls.add((x, y))
            elif c == '.':
                # ignore
                pass
            elif c in ('G', 'E'):
                characters.append(Character(
                    type=CharacterType.Goblin if c == 'G' else CharacterType.Elf,
                    attack_power=goblin_attack_power if c == 'G' else elf_attack_power,
                    hit_points=200,
                    position=(x, y)
                ))
    return State(walls=walls, characters=tuple(characters))


def manhattan_distance(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def is_reachable(start: Position, end: Position, blockages: Set[Position]) -> bool:
    # TODO: use A* instead of BFS
    queue = deque([start])
    seen = set()
    while len(queue) > 0:
        cur = queue.popleft()
        if cur in seen:
            continue
        elif cur == end:
            return True
        seen.add(cur)
        queue.extend(p for p in adjacent_positions(cur) if p not in blockages)
    return False


def shortest_path(start: Position, end: Position, blockages: Set[Position]) -> Tuple[Position, ...]:
    # modified dijkstra algorithm
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
            if edge in blockages:
                continue

            if edge not in visited:
                nodes.add(edge)

            weight = current_weight + manhattan_distance(min_node, edge)
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node
            elif weight == visited[edge] and position_is_before(min_node, path[edge]):
                # if weights are equal, pick the one that is first in reading order
                path[edge] = min_node

    stack = deque()
    u = end
    while u is not None:
        stack.appendleft(u)
        u = path.get(u, None)

    return tuple(stack)


def position_is_before(a: Position, b: Position) -> bool:
    # `a` is before `b`, in reading order (top-to-bottom, then left-to-right)
    return (a[1], a[0]) < (b[1], b[0])


def sort_characters(characters: Iterable[Character]) -> Tuple[Character]:
    # sort in reading order (top-to-bottom, then left-to-right)
    return tuple(sorted(characters, key=lambda c: (c.position[1], c.position[0])))


def perform_move(character: Character, opponents: Iterable[Character], tiles: Set[Position]) -> Optional[Character]:
    character_adjacent_positions = character.adjacent_positions()

    # determine target position to move to
    possible_positions = []
    has_opponent_in_range = False
    for target in opponents:
        if target.position in character_adjacent_positions:
            has_opponent_in_range = True
            break

        for position in target.adjacent_positions():
            if position in tiles:
                # this is not a valid position
                continue
            elif not is_reachable(character.position, position, tiles):
                # obstruction ahead
                continue
            possible_positions.append(position)

    if has_opponent_in_range:
        # don't move, we are already ready for combat
        return None

    # determine the best target
    best_path = None
    for target in possible_positions:
        path = shortest_path(character.position, target, tiles)
        if best_path is None or len(path) < len(best_path):
            best_path = path
        elif len(path) == len(best_path) and position_is_before(path[-1], best_path[-1]):
            best_path = path

    if best_path is None:
        # we have nowhere to go to
        return None

    # determine next move
    new_position = best_path[1]

    # perform move
    return character._replace(position=new_position)


# test 1 for perform_move()
_ = parse_state("""
#######
#E..G.#
#...#.#
#.G.#G#
#######""".strip())
assert perform_move(
    next(c for c in _.characters if c.type == CharacterType.Elf),
    tuple(c for c in _.characters if c.type == CharacterType.Goblin),
    set(_.tiles().keys())
).position == (2, 1)

# test 2 for perform_move()
_ = parse_state("""
#######
#.E...#
#.....#
#...G.#
#######""".strip())
assert perform_move(
    next(c for c in _.characters if c.type == CharacterType.Elf),
    tuple(c for c in _.characters if c.type == CharacterType.Goblin),
    set(_.tiles().keys())
).position == (3, 1)


def find_attack_target(character: Character, opponents: Iterable[Character]) -> Optional[Character]:
    character_adjacent_positions = character.adjacent_positions()
    target = None
    for other in opponents:
        if other.position not in character_adjacent_positions:
            continue

        if target is None or other.hit_points < target.hit_points:
            target = other
        elif other.hit_points == target.hit_points and position_is_before(other, target):
            target = other
    return target


def advance_state(state: State) -> Tuple[State, bool]:
    tiles = set(state.tiles().keys())
    characters = set(state.characters)
    seen_characters = set()
    was_full_round = True
    while len(characters - seen_characters) > 0:
        character = sort_characters(characters - seen_characters)[0]
        seen_characters.add(character)

        opponents = sort_characters(c for c in characters if c.type == character.type.opponent)
        if len(opponents) == 0:
            # nothing to do anymore
            was_full_round = False
            break

        # character moves, if needed
        new_character = perform_move(character, opponents, tiles)

        if new_character is not None:
            # update characters set
            characters.remove(character)
            characters.add(new_character)
            seen_characters.add(new_character)

            # update tiles
            tiles.remove(character.position)
            tiles.add(new_character.position)

            # update local variable
            character = new_character

        # determine potential target
        attack_target = find_attack_target(character, opponents)
        if attack_target is not None:
            # attack target
            new_hp = attack_target.hit_points - character.attack_power
            new_attack_target = attack_target._replace(hit_points=new_hp)

            # update characters set
            characters.remove(attack_target)
            if new_attack_target.hit_points > 0:
                characters.add(new_attack_target)
                if attack_target in seen_characters:
                    seen_characters.add(new_attack_target)
            else:
                # update tiles
                tiles.remove(attack_target.position)

    return state._replace(characters=tuple(characters)), was_full_round


# test movement
_ = parse_state("""
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########""".strip())
_ = advance_state(_)[0]
assert str(_) == """
#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########""".strip()
_ = advance_state(_)[0]
assert str(_) == """
#########
#..G.G..#
#...G...#
#.G.E.G.#
#.......#
#G..G..G#
#.......#
#.......#
#########""".strip()
_ = advance_state(_)[0]
assert str(_) == """
#########
#.......#
#..GGG..#
#..GEG..#
#G..G...#
#......G#
#.......#
#.......#
#########""".strip()

# test attack
_ = parse_state("""
#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""".strip())
_hp = lambda state: [f"{str(c)}({c.hit_points})" for c in sort_characters(state.characters)]

_ = advance_state(_)[0]
assert _hp(_) == ["G(200)", "E(197)", "G(197)", "G(200)", "G(197)", "E(197)"]
_ = advance_state(_)[0]
assert _hp(_) == ["G(200)", "G(200)", "E(188)", "G(194)", "G(194)", "E(194)"]
for __ in range(21):
    _ = advance_state(_)[0]
assert _hp(_) == ["G(200)", "G(200)", "G(131)", "G(131)", "E(131)"]
_ = advance_state(_)[0]
assert _hp(_) == ["G(200)", "G(131)", "G(200)", "G(128)", "E(128)"]
_ = advance_state(_)[0]
assert _hp(_) == ["G(200)", "G(131)", "G(125)", "G(200)", "E(125)"]
_ = advance_state(_)[0]
assert _hp(_) == ["G(200)", "G(131)", "G(122)", "E(122)", "G(200)"]
_ = advance_state(_)[0]
assert _hp(_) == ["G(200)", "G(131)", "G(119)", "E(119)", "G(200)"]
_ = advance_state(_)[0]
assert _hp(_) == ["G(200)", "G(131)", "G(116)", "E(113)", "G(200)"]
for __ in range(19):
    _ = advance_state(_)[0]
assert _hp(_) == ["G(200)", "G(131)", "G(59)", "G(200)"]

# testcases from https://www.reddit.com/r/adventofcode/comments/a6rhzw/help_need_help_with_day_15_part_1/ebxk3v5/
_ = parse_state("""
#######
#######
#.E..G#
#.#####
#G#####
#######
#######""".strip())
_ = advance_state(_)[0]
assert next(c for c in _.characters if c.type == CharacterType.Elf).position == (3, 2)

_ = parse_state("""
####
#GG#
#.E#
####""".strip())
_ = advance_state(_)[0]
assert _hp(_) == ["G(197)", "G(200)", "E(194)"]

_ = parse_state("""
########
#..E..G#
#G######
########""".strip())
_ = advance_state(_)[0]
assert next(c for c in _.characters if c.type == CharacterType.Elf).position == (2, 1)
