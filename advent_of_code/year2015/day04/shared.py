from hashlib import md5


def find_index(text: str, number_of_leading_zeroes: int) -> int:
    idx = 0
    prefix = "0" * number_of_leading_zeroes
    while True:
        hash = md5(f"{text}{idx}".encode("utf8")).hexdigest()
        if hash.startswith(prefix):
            return idx
        idx += 1
