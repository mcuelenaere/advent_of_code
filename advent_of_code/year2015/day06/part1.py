from .shared import parse_lines, execute_light_configuration


def action_parser(action: str) -> callable:
    if action == 'turn on':
        return lambda val: True
    elif action == 'turn off':
        return lambda val: False
    elif action == 'toggle':
        return lambda val: not val
    else:
        raise ValueError(f"Invalid action {action}")


def calculate(text: str) -> int:
    lines = parse_lines(text.splitlines())
    light_configuration = execute_light_configuration(lines, False, action_parser)
    return sum(1 if x else 0 for row in light_configuration for x in row)


assert calculate("turn on 0,0 through 999,999") == 1_000_000
