from .shared import as_matrix, follow_path


def calculate(text: str) -> str:
    m = as_matrix(text)
    return "".join(c for c in follow_path(m) if c.isalpha())


puzzle = """
     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+
""".strip(
    "\n"
)
assert calculate(puzzle) == "ABCDEF"
