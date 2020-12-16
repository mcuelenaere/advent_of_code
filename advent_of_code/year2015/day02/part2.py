def calculate(text: str) -> int:
    def solve(l: int, w: int, h: int) -> int:
        # find smallest sides
        side1, side2 = tuple(sorted([l, w, h]))[:2]
        return side1 * 2 + side2 * 2 + l * w * h

    dimensions = (map(int, x.split("x")) for x in text.splitlines())
    return sum(solve(l, w, h) for l, w, h in dimensions)


assert calculate("2x3x4") == 34
assert calculate("1x1x10") == 14
