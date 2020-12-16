from .shared import tie_knots, sparse_to_dense


def calculate(text: str) -> str:
    lengths = list(map(lambda x: ord(x), text))
    lengths.extend([17, 31, 73, 47, 23])

    sparse = tie_knots(256, lengths, rounds=64)
    dense = sparse_to_dense(sparse)
    formatted = ''.join('%02x' % x for x in dense)
    return formatted


testcases = {
    '': 'a2582a3a0e66e6e86e3812dcb672a272',
    'AoC 2017': '33efeb34ea91902bb2f59c9920caa6cd',
    '1,2,3': '3efbe78a8d82f29979031a4aa0b16a9d',
    '1,2,4': '63960835bcdc130f0b66d7ff4f6a5a8e',
}
for input, expected in testcases.items():
    assert calculate(input) == expected
