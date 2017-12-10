def calculate(text: str) -> int:
    houses_visited = set()

    def visit_houses(path):
        pos = [0, 0]
        houses_visited.add(tuple(pos))
        for x in path:
            if x == '>':
                pos[0] += 1
            elif x == '<':
                pos[0] -= 1
            elif x == '^':
                pos[1] -= 1
            elif x == 'v':
                pos[1] += 1
            houses_visited.add(tuple(pos))

    # Santa
    visit_houses(text[::2])

    # Robo-Santa
    visit_houses(text[1::2])

    return len(houses_visited)


assert calculate("^v") == 3
assert calculate("^>v<") == 3
assert calculate("^v^v^v^v^v") == 11
