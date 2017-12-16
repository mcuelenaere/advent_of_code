from .shared import parse_lines, execute_light_configuration


def action_parser(action: str) -> callable:
    if action == 'turn on':
        return lambda val: val + 1
    elif action == 'turn off':
        return lambda val: max(val - 1, 0)
    elif action == 'toggle':
        return lambda val: val + 2
    else:
        raise ValueError(f"Invalid action {action}")


def calculate(text: str) -> int:
    lines = parse_lines(text.splitlines())
    light_configuration = execute_light_configuration(lines, 0, action_parser)
    return sum(x for row in light_configuration for x in row)


assert calculate("toggle 0,0 through 999,999") == 2_000_000
