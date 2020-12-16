from .shared import find_next_valid_password, is_valid_password


def calculate(text: str) -> str:
    return find_next_valid_password(text)


assert not is_valid_password('hijklmmn')
assert not is_valid_password('abbceffg')
assert not is_valid_password('abbcegjk')
assert calculate('bcdefgh') == 'bcdffaa'
assert calculate('ghijklmn') == 'ghjaabcc'
