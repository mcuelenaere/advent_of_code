from .shared import parse_text
from operator import gt, eq, lt

MFCSAM_OUTPUT = """
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
""".strip()
MFCSAM_OUTPUT = {line.split(': ')[0]: int(line.split(': ')[1]) for line in MFCSAM_OUTPUT.splitlines()}

COMPARISON_OPS = {
    'children': eq,
    'cats': gt,
    'samoyeds': eq,
    'pomeranians': lt,
    'akitas': eq,
    'vizslas': eq,
    'goldfish': lt,
    'trees': gt,
    'cars': eq,
    'perfumes': eq,
}


def calculate(text: str) -> int:
    for sue_number, properties in parse_text(text):
        is_match = all(COMPARISON_OPS[k](v, MFCSAM_OUTPUT[k]) for k, v in properties.items())
        if is_match:
            return sue_number
