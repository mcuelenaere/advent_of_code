from itertools import chain
from .shared import extract_image_layers


def calculate(text: str) -> int:
    digits = tuple(map(int, text))
    layers = extract_image_layers(digits, 25, 6)
    scores = []
    for layer in layers:
        zero_count = sum(1 for digit in chain.from_iterable(layer) if digit == 0)
        one_count = sum(1 for digit in chain.from_iterable(layer) if digit == 1)
        two_count = sum(1 for digit in chain.from_iterable(layer) if digit == 2)
        scores.append((zero_count, one_count * two_count))
    return min(scores, key=lambda x: x[0])[1]
