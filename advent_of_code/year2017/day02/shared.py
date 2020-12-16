def parse_line(line: str):
    return tuple(map(int, line.split("\t")))


def parse_input(text: str):
    return tuple(parse_line(line) for line in text.splitlines())
