def calculate(text: str) -> int:
    houses_visited = set()

    pos = [0, 0]
    houses_visited.add(tuple(pos))
    for x in text:
        if x == ">":
            pos[0] += 1
        elif x == "<":
            pos[0] -= 1
        elif x == "^":
            pos[1] -= 1
        elif x == "v":
            pos[1] += 1
        houses_visited.add(tuple(pos))

    return len(houses_visited)


assert calculate(">") == 2
assert calculate("^>v<") == 4
assert calculate("^v^v^v^v^v") == 2
