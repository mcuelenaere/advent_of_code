from .shared import parse_data
from collections import defaultdict
from functools import reduce


def calculate(text: str) -> int:
    rules, your_ticket, nearby_tickets = parse_data(text)

    # determine valid tickets
    valid_tickets = []
    for ticket in nearby_tickets:
        ticket_is_valid = True
        for field in ticket:
            field_is_valid = False
            for rule in rules:
                field_is_valid |= any(bounds.min <= field <= bounds.max for bounds in rule.bounds)
            ticket_is_valid &= field_is_valid
        if ticket_is_valid:
            valid_tickets.append(ticket)
    valid_tickets.append(your_ticket)

    # determine which fields rules can apply to
    applicable_rules = defaultdict(set)
    for rule in rules:
        bounds = rule.bounds
        for i in range(len(rules)):
            is_valid = all(bounds[0].min <= ticket[i] <= bounds[0].max or
                           bounds[1].min <= ticket[i] <= bounds[1].max for ticket in valid_tickets)
            if is_valid:
                applicable_rules[i].add(rule)

    # reduce duplicates until only a single rule per field remains
    while any(len(x) > 1 for x in applicable_rules.values()):
        single_rules = set(next(iter(v)) for k, v in applicable_rules.items() if len(v) == 1)
        for rules in applicable_rules.values():
            if len(rules) == 1:
                continue
            rules.difference_update(single_rules)
    ordered_rules = {idx: next(iter(rules)) for idx, rules in applicable_rules.items()}

    # multiply departure fields
    departure_fields = tuple(your_ticket[idx] for idx, rule in ordered_rules.items() if rule.name.startswith('departure'))
    assert len(departure_fields) == 6
    return reduce(lambda x, y: x * y, departure_fields)
