def calculate(text: str) -> int:
    floor = 0
    for index, char in enumerate(text):
        if char == "(":
            floor += 1
        elif char == ")":
            floor += -1
        else:
            raise ValueError()

        if floor == -1:
            return index + 1


testcases = {
    ")": 1,
    "()())": 5,
}
for input, expected in testcases.items():
    assert calculate(input) == expected
