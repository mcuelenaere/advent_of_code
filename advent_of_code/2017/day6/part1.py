from .shared import redistribute, parse


def calculate(text: str) -> int:
    banks = parse(text)
    already_seen = set()
    counter = 0
    while tuple(banks) not in already_seen:
        already_seen.add(tuple(banks))
        banks = redistribute(banks)
        counter += 1
    return counter


assert calculate("0	2	7	0") == 5
