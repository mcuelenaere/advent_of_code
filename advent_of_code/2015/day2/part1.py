def calculate(text: str) -> int:
    dimensions = (map(int, x.split('x')) for x in text.splitlines())
    return sum(2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, h*l) for l, w, h in dimensions)


assert calculate("2x3x4") == 58
assert calculate("1x1x10") == 43
