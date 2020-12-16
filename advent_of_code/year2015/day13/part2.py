from .shared import find_maximum_happiness, parse_text


def calculate(text: str) -> int:
    config = parse_text(text)

    # add ourselves
    for other in {x[0] for x in config.keys()}:
        config[("ourself", other)] = 0
        config[(other, "ourself")] = 0

    return find_maximum_happiness(config)
