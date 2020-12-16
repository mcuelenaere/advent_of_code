from typing import Iterable, Tuple


ImageLayer = Tuple[Tuple[int, ...], ...]


def extract_image_layers(digits: Tuple[int, ...], width: int, height: int) -> Iterable[ImageLayer]:
    for n in range(0, len(digits), width * height):
        layer = []
        for start in range(n, n + width * height, width):
            layer.append(digits[start : start + width])
        yield tuple(layer)


assert tuple(extract_image_layers((1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2), 3, 2)) == (
    ((1, 2, 3), (4, 5, 6)),
    ((7, 8, 9), (0, 1, 2)),
)
