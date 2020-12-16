def calculate(text: str) -> int:
    return sum(map(int, text.splitlines()))


puzzle = """
+1
-2
+3
+1
""".strip()
assert calculate(puzzle) == 3
