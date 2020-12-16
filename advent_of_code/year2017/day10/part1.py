from .shared import tie_knots


def calculate(text: str, list_length: int = 256) -> int:
    lengths = map(int, text.split(','))
    result = tie_knots(list_length, lengths)
    return result[0] * result[1]


assert calculate('3,4,1,5', 5) == 12
