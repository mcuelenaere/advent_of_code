def calculate(text: str) -> int:
    entries = tuple(map(int, text.splitlines()))

    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            for k in range(j + 1, len(entries)):
                if entries[i] + entries[j] + entries[k] == 2020:
                    return entries[i] * entries[j] * entries[k]


_input = """1721
979
366
299
675
1456
""".strip()
assert calculate(_input) == 241861950
