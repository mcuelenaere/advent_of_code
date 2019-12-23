from .shared import parse_map, calculate_alignment_parameters


def calculate(text: str) -> int:
    scaffolds, robot_position, robot_direction = parse_map(text)
    # fixup broken robot direction
    robot_direction = (1, 0)
    return calculate_alignment_parameters(scaffolds, robot_position, robot_direction)

