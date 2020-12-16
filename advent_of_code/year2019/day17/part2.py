from collections import defaultdict
from typing import Tuple

from .shared import ConfigurableVacuumRobot, compress_path, walk_path


def build_functions(path: Tuple[str]):
    # build frequency table
    freq_table = defaultdict(set)
    for n in range(2, min(len(path), 20) + 1):
        for offset in range(0, n + 1):
            for i in range(offset, len(path), n):
                freq_table[path[i : i + n]].add(i)

    # build inverse table
    inverse_table = defaultdict(set)
    for key, indices in freq_table.items():
        if len(indices) == 1:
            continue
        for index in indices:
            if path[index : index + len(key)] != key:
                continue
            inverse_table[index].add(key)

    # perform DFS to find possible solutions
    def dfs(index: int = 0, stack: Tuple[str] = tuple()):
        if index > len(path):
            # too long, this solution is invalid
            return
        elif len(set(stack)) > 3:
            # early abort, more than 3 functions created
            return
        elif index == len(path):
            # this solution is correct
            yield stack
            return

        for option in inverse_table[index]:
            yield from dfs(index + len(option), stack + (option,))

    solutions = tuple(dfs())

    # pick first solution and convert it to a better format
    assert len(solutions) > 0
    parts = solutions[0]
    functions = dict(zip("ABC", set(parts)))
    routine = tuple(next(name for name, fn in functions.items() if fn == fn_to_find) for fn_to_find in parts)
    return functions, routine


def calculate(intcode_instructions: str) -> int:
    vacuum_robot = ConfigurableVacuumRobot(intcode_instructions)

    # parse the map
    scaffolds, robot_position, robot_direction = vacuum_robot.parse_map()
    robot_direction = (1, 0)  # fixup broken robot direction

    # find the path to walk
    path = tuple(dir for dir, pos in walk_path(scaffolds, robot_position, robot_direction))

    # build the movement function routines
    path = tuple(compress_path(path))
    functions, routine = build_functions(path)

    # execute movement instructions
    movement_instructions = (
        ",".join(routine),
        ",".join(functions["A"]),
        ",".join(functions["B"]),
        ",".join(functions["C"]),
    )
    return vacuum_robot.execute_movement_routine(movement_instructions)
