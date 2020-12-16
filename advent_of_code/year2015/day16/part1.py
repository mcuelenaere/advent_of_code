from .shared import parse_text

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


def calculate(text: str) -> int:
    for sue_number, properties in parse_text(text):
        is_match = all(MFCSAM_OUTPUT[k] == v for k, v in properties.items())
        if is_match:
            return sue_number
