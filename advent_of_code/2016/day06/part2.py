from .shared import sorted_freq_count, parse_columns


def calculate(text: str) -> str:
    columns = parse_columns(text)
    return ''.join(sorted_freq_count(col)[-1] for col in columns)


puzzle = """
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
""".strip()
assert calculate(puzzle) == "advent"
