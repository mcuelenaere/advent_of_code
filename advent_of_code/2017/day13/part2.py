from .shared import parse, Firewall


def try_combination(firewall: Firewall, delay: int) -> bool:
    firewall.timestamp = delay
    for player_position in range(firewall.width + 1):
        if firewall.is_caught(player_position):
            #print(delay, 'failed at', player_position)
            return False
        firewall.execute_step()
    return True


def calculate(text: str) -> int:
    firewall = parse(text)

    # bruteforce all combinations
    for delay in range(100):
        print("%03d" % delay, "  ", " ".join("%02d" % firewall.scanner_positions[x] if x in firewall.scanner_positions else '..' for x in range(firewall.width + 1)), "->", set(p for p in range(firewall.width + 1) if firewall.is_caught(p)))
        firewall.execute_step()
        #if try_combination(firewall, delay):
        #    return delay

    raise RuntimeError('Could not find the right delay!')


puzzle = """
0: 3
1: 2
4: 4
6: 4
""".strip()
assert calculate(puzzle) == 10
