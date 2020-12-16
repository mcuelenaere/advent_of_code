from .shared import as_matrix, follow_path


def calculate(text: str) -> int:
    m = as_matrix(text)
    return sum(1 for c in follow_path(m))


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
assert calculate(puzzle) == 38
