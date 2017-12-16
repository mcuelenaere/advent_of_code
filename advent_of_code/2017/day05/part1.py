def calculate(text: str) -> int:
    offsets = list(map(int, text.splitlines()))
    counter = 0
    index = 0
    while index < len(offsets):
        old_index = index
        index += offsets[index]
        offsets[old_index] += 1
        counter += 1
    return counter


puzzle = """
0
3
0
1
-3
""".strip()
assert calculate(puzzle) == 5
