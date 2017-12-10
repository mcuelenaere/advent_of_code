def calculate(text: str) -> int:
    s = 0
    for line in text.splitlines():
        string_code_length = len(line)
        in_memory_length = len(eval(line))
        s += string_code_length - in_memory_length
    return s


puzzle = r"""
""
"abc"
"aaa\"aaa"
"\x27"
""".strip()
assert calculate(puzzle) == 12
