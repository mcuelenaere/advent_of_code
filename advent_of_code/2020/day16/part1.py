from .shared import parse_data


def calculate(text: str) -> int:
    rules, _, nearby_tickets = parse_data(text)

    invalid_values_sum = 0
    for ticket in nearby_tickets:
        for field in ticket:
            is_valid = False
            for rule in rules:
                is_valid |= any(bounds.min <= field <= bounds.max for bounds in rule.bounds)
            if not is_valid:
                invalid_values_sum += field

    return invalid_values_sum


puzzle = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
assert calculate(puzzle) == 71
