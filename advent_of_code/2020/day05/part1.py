from .shared import decode_seat_id


def calculate(text: str) -> int:
    return max(decode_seat_id(line) for line in text.splitlines())
