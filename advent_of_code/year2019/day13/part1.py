from ..day05.shared import parse_instructions, streaming_evaluate


def calculate(text: str) -> int:
    instructions = parse_instructions(text)
    gen = streaming_evaluate(instructions)

    # run program
    tiles = {}
    while True:
        try:
            x = next(gen)
            y = next(gen)
            tile_id = next(gen)
            tiles[(x, y)] = tile_id
        except StopIteration:
            break

    return sum(1 for tile_id in tiles.values() if tile_id == 2)
