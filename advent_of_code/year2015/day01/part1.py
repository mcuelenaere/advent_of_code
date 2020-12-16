def calculate(text: str) -> int:
    floor = 0
    for char in text:
        if char == "(":
            floor += 1
        elif char == ")":
            floor += -1
        else:
            raise ValueError()
    return floor


testcases = {
    "(())": 0,
    "()()": 0,
    "(((": 3,
    "(()(()(": 3,
    "))(((((": 3,
    "())": -1,
    "))(": -1,
    ")))": -3,
    ")())())": -3,
}
for input, expected in testcases.items():
    assert calculate(input) == expected
