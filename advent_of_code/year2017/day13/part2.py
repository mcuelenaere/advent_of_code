from .shared import Firewall, parse


def try_combination(firewall: Firewall, delay: int) -> bool:
    for scanner_position in firewall.scanner_positions:
        firewall.timestamp = delay + scanner_position
        if firewall.is_caught(scanner_position):
            return False
    return True


def calculate(text: str) -> int:
    firewall = parse(text)

    # bruteforce all combinations
    delay = 0
    while True:
        if try_combination(firewall, delay):
            return delay
        else:
            delay += 1


puzzle = """
0: 3
1: 2
4: 4
6: 4
""".strip()
assert calculate(puzzle) == 10
