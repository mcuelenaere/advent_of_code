from itertools import chain
from .shared import parse_ips, find_abas


def calculate(text: str) -> int:
    has_ssl = 0
    for ip in parse_ips(text):
        abas = set(chain.from_iterable(find_abas(t) for t in ip.supernet_sequences))
        babs = set(chain.from_iterable(find_abas(t) for t in ip.hypernet_sequences))

        for aba in abas:
            bab = aba[1] + aba[0] + aba[1]
            if bab in babs:
                has_ssl += 1
                break
    return has_ssl


puzzle = """
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
""".strip()
assert calculate(puzzle) == 3
