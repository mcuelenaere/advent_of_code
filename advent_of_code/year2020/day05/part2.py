from .shared import decode_seat_id


def calculate(text: str) -> int:
    seat_ids = set(decode_seat_id(line) for line in text.splitlines())

    for seat_id in range(min(seat_ids), max(seat_ids) + 1):
        if seat_id not in seat_ids:
            return seat_id
