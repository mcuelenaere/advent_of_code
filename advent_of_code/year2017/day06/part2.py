from .shared import parse, redistribute


def calculate(text: str) -> int:
    banks = parse(text)
    already_seen = set()
    while tuple(banks) not in already_seen:
        already_seen.add(tuple(banks))
        banks = redistribute(banks)
    banks_to_look_for = banks.copy()
    counter = 1
    banks = redistribute(banks)
    while banks != banks_to_look_for:
        banks = redistribute(banks)
        counter += 1
    return counter


assert calculate("0	2	7	0") == 4
