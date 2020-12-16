from .shared import find_root, parse_lines


def calculate(text: str) -> str:
    lines = text.splitlines()
    return find_root(parse_lines(lines))


puzzle = """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
""".strip()

assert calculate(puzzle) == "tknk"
