from .shared import find_abbas, parse_ips


def calculate(text: str) -> int:
    has_tls = 0
    for ip in parse_ips(text):
        supernet_seq_count = sum(len(find_abbas(t)) for t in ip.supernet_sequences)
        hypernet_seq_count = sum(len(find_abbas(t)) for t in ip.hypernet_sequences)
        if supernet_seq_count > 0 and hypernet_seq_count == 0:
            has_tls += 1
    return has_tls


puzzle = """
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
""".strip()
assert calculate(puzzle) == 2
