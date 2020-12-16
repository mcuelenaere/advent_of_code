def hamming_distance(s1: str, s2: str) -> int:
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


def calculate(text: str) -> str:
    boxes = text.splitlines()

    # bruteforce approach
    for box1 in boxes:
        for box2 in boxes:
            if box1 == box2:
                continue

            if hamming_distance(box1, box2) == 1:
                # found the correct boxes, determine the common characters
                return ''.join(a for a, b in zip(box1, box2) if a == b)

    raise RuntimeError('Could not find boxes with hamming distance == 1')


puzzle = """
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
""".strip()
assert calculate(puzzle) == 'fgij'
