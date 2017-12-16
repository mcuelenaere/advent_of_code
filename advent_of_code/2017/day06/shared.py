def redistribute(banks):
    max_idx = next(i for i, x in enumerate(banks) if x == max(banks))
    block_count = banks[max_idx]
    banks[max_idx] = 0

    idx = max_idx
    for _ in range(block_count):
        idx = (idx + 1) % len(banks)
        banks[idx] += 1

    return banks


def parse(text: str):
    return list(map(int, text.split("\t")))
