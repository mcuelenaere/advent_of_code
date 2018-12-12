from typing import Tuple, Dict


def parse_input(text: str) -> Tuple[str, Dict[str, str]]:
    lines = text.splitlines()
    initial_state = lines[0].split('initial state: ')[1]

    transformations = {}
    for line in lines[2:]:
        _from, _to = line.split(' => ')
        transformations[_from] = _to

    return initial_state, transformations


def transform(text: str, transformations: Dict[str, str]) -> str:
    chars = list(text)
    for i in range(2, len(text) - 2):
        m = transformations.get(text[i - 2:i + 3], None)
        if m:
            chars[i] = m
        else:
            chars[i] = '.'
    return ''.join(chars)
