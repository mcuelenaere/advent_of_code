def escape(line: str) -> str:
    line = line.translate(
        line.maketrans(
            {
                '"': r"\"",
                "\\": "\\\\",
            }
        )
    )
    return f'"{line}"'


def calculate(text: str) -> int:
    s = 0
    for line in text.splitlines():
        string_code_length = len(line)
        encoded_string_length = len(escape(line))
        s += encoded_string_length - string_code_length
    return s


assert escape(r'""') == r'"\"\""'
assert escape(r'"abc"') == r'"\"abc\""'
assert escape(r'"aaa\"aaa"') == r'"\"aaa\\\"aaa\""'
assert escape(r'"\x27"') == r'"\"\\x27\""'

puzzle = r"""
""
"abc"
"aaa\"aaa"
"\x27"
""".strip()
assert calculate(puzzle) == 19
