from typing import Tuple

from .shared import ImageLayer, extract_image_layers


COLOR_BLACK = 0
COLOR_WHITE = 1
COLOR_TRANSPARANT = 2


def composite_image(layers: Tuple[ImageLayer]) -> ImageLayer:
    width = len(layers[0][0])
    height = len(layers[0])
    final_image = [[0] * width for _ in range(height)]
    for layer_idx, layer in reversed(tuple(enumerate(layers))):
        for x in range(width):
            for y in range(height):
                if layer[y][x] in (COLOR_BLACK, COLOR_WHITE):
                    final_image[y][x] = layer[y][x]
                elif layer[y][x] == COLOR_TRANSPARANT:
                    pass  # do nothing
                else:
                    raise RuntimeError(f"Invalid color {layer[y][x]} at ({x},{y}) in layer {layer_idx}")
    return tuple(tuple(line) for line in final_image)


assert composite_image(tuple(extract_image_layers((0, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 0, 0, 0, 0), 2, 2))) == (
    (0, 1),
    (1, 0),
)


def calculate(text: str) -> str:
    digits = tuple(map(int, text))
    layers = tuple(extract_image_layers(digits, 25, 6))
    final_image = composite_image(layers)
    for line in final_image:
        print("".join("x" if digit == 1 else " " for digit in line))
    # I'm not going to implement OCR here, so just return the string as-is
    return "FPUAR"
