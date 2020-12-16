from .shared import parse_lumber_area, advance_lumber_area, freq_count, ACRE_TREE, ACRE_LUMBERYARD


def calculate(text: str) -> int:
    lumber_area = parse_lumber_area(text)
    last_seen_areas = [lumber_area]
    cycle_duration = None
    for i in range(1000000000):
        lumber_area = advance_lumber_area(lumber_area)
        if lumber_area in last_seen_areas:
            # cycle detected, break from loop
            cycle_duration = len(last_seen_areas) - last_seen_areas.index(lumber_area)
            break
        last_seen_areas.append(lumber_area)
    assert cycle_duration is not None

    # skip ((1000000000 - i) // cycle_duration) cycles

    # advance the remaining iterations
    for _ in range((1000000000 - i) % cycle_duration - 1):
        lumber_area = advance_lumber_area(lumber_area)

    acre_count = freq_count(lumber_area.values())
    return acre_count[ACRE_TREE] * acre_count[ACRE_LUMBERYARD]
