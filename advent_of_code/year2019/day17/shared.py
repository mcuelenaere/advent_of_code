from typing import Iterable, Set, Tuple

from ..day05.shared import parse_instructions, streaming_evaluate


Position = Tuple[int, int]

ROBOT_DIRECTIONS_MAP = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}

SORTED_DIRECTIONS = (
    (0, -1),  # up
    (1, 0),  # right
    (0, 1),  # down
    (-1, 0),  # left
)


def parse_text(text: Iterable[str]) -> Tuple[Set[Position], Position, Position]:
    scaffolds = set()
    robot_position = None
    robot_direction = None
    x = 0
    y = 0
    for char in text:
        if char == "\n":
            x = 0
            y += 1
        elif char == "#":
            scaffolds.add((x, y))
            x += 1
        elif char in ("^", "v", "<", ">"):
            robot_position = (x, y)
            robot_direction = ROBOT_DIRECTIONS_MAP[char]
            x += 1
        elif char == ".":
            x += 1
        else:
            raise RuntimeError(f'unknown char "{char}')

    return scaffolds, robot_position, robot_direction


def parse_map(text: str) -> Tuple[Set[Position], Position, Position]:
    instructions = parse_instructions(text)
    return parse_text(chr(char) for char in streaming_evaluate(instructions))


def walk_path(
    scaffolds: Set[Position], robot_position: Position, robot_direction: Position
) -> Iterable[Tuple[Position, Position]]:
    # move robot onto first scaffold
    robot_position = (
        robot_position[0] + robot_direction[0],
        robot_position[1] + robot_direction[1],
    )
    yield robot_direction, robot_position

    seen_scaffolds = {
        robot_position,
    }
    while True:
        # go same direction, if possible
        new_pos = (
            robot_position[0] + robot_direction[0],
            robot_position[1] + robot_direction[1],
        )
        if new_pos in scaffolds:
            # all okay, move on
            seen_scaffolds.add(new_pos)
            robot_position = new_pos
            yield robot_direction, robot_position
            continue

        # no more scaffolds available, have to find a new direction
        for new_direction in ROBOT_DIRECTIONS_MAP.values():
            new_pos = (
                robot_position[0] + new_direction[0],
                robot_position[1] + new_direction[1],
            )
            if new_pos in seen_scaffolds or new_pos not in scaffolds:
                continue

            # found one!
            robot_direction = new_direction
            break
        else:
            # reached the end of the level
            break


def calculate_alignment_parameters(
    scaffolds: Set[Position],
    initial_robot_position: Position,
    initial_robot_direction: Position,
) -> int:
    intersections = set()
    for _, position in walk_path(scaffolds, initial_robot_position, initial_robot_direction):
        # check if we are at an intersection
        surrounded_by_scaffolds = all(
            (position[0] + direction[0], position[1] + direction[1]) in scaffolds
            for direction in ROBOT_DIRECTIONS_MAP.values()
        )
        if surrounded_by_scaffolds:
            intersections.add(position)

    return sum(x * y for x, y in intersections)


_ = parse_text(
    """..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^.."""
)
assert calculate_alignment_parameters(*_) == 76


def compress_path(directions: Iterable[Position]) -> Iterable[str]:
    # robot starts facing upwards
    last = (0, -1)
    counter = 0

    for direction in directions:
        if direction == last:
            counter += 1
        else:
            if counter > 0:
                yield str(counter + 1)

            # calculate rotation
            diff = SORTED_DIRECTIONS.index(direction) - SORTED_DIRECTIONS.index(last)
            if abs(diff) == 3:
                yield "R" if diff == -3 else "L"
            elif abs(diff) == 2:
                # always try turning to the right; picking the same direction
                # potentially allows for better compressability
                yield "R"
                yield "R"
            elif abs(diff) == 1:
                yield "L" if diff == -1 else "R"

            # reset internal state
            last = direction
            counter = 0

    if counter > 0:
        yield str(counter + 1)


_ = parse_text(
    """#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
>########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......"""
)
assert tuple(compress_path(dir for dir, pos in walk_path(*_))) == (
    "R",
    "8",
    "R",
    "8",
    "R",
    "4",
    "R",
    "4",
    "R",
    "8",
    "L",
    "6",
    "L",
    "2",
    "R",
    "4",
    "R",
    "4",
    "R",
    "8",
    "R",
    "8",
    "R",
    "8",
    "L",
    "6",
    "L",
    "2",
)


class ConfigurableVacuumRobot(object):
    def __init__(self, instructions: str):
        self._instructions = parse_instructions(instructions)
        assert self._instructions[0] == 1
        self._instructions[0] = 2
        self._cpu = streaming_evaluate(self._instructions)

    def parse_map(self):
        buf = ""
        while len(buf) < 2 or buf[-2:] != "\n\n":
            buf += chr(next(self._cpu))
        return parse_text(buf)

    def execute_movement_routine(self, movement_instructions: Tuple[str, ...]) -> int:
        def expect(expected: str):
            for letter in expected:
                letter = ord(letter)
                actual = next(self._cpu)
                assert actual == letter, f"Got {chr(actual)}, expected {chr(letter)}"

        def send_and_expect(input_letter: str, expected_letter: str):
            assert len(input_letter) == 1 and len(expected_letter) == 1
            assert self._cpu.send(ord(input_letter)) == ord(expected_letter)

        def send(input: str):
            for letter in input:
                letter = ord(letter)
                res = self._cpu.send(letter)
                assert res is None or res == ord("\n"), f"Expected None or \\n, got {chr(res)}"

        expect("Main:\n")
        send("\n")
        send(movement_instructions[0])
        send_and_expect("\n", "F")
        expect("unction A:\n")
        send("\n")
        send(movement_instructions[1])
        send_and_expect("\n", "F")
        expect("unction B:\n")
        send("\n")
        send(movement_instructions[2])
        send_and_expect("\n", "F")
        expect("unction C:\n")
        send("\n")
        send(movement_instructions[3])
        send_and_expect("\n", "C")
        expect("ontinuous video feed?\n")
        send("\nn\n")

        # discard output and only keep non-ASCII value
        while True:
            res = next(self._cpu)
            if res > 0xFF:
                return res
