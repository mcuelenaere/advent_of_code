from collections import defaultdict


def calculate(lines: str) -> int:
    path = defaultdict(set)

    def parse_wire(wire: str, id: str):
        cur_x = 0
        cur_y = 0
        steps = 0
        path_steps = {}
        for objective in wire.split(','):
            direction = objective[0]
            distance = int(objective[1:])
            if direction == 'R':
                for x in range(cur_x, cur_x + distance):
                    path[(x, cur_y)].add(id)
                    path_steps[(x, cur_y)] = steps
                    steps += 1
                cur_x += distance
            elif direction == 'L':
                for x in range(cur_x, cur_x - distance, -1):
                    path[(x, cur_y)].add(id)
                    path_steps[(x, cur_y)] = steps
                    steps += 1
                cur_x -= distance
            elif direction == 'U':
                for y in range(cur_y, cur_y - distance, -1):
                    path[(cur_x, y)].add(id)
                    path_steps[(cur_x, y)] = steps
                    steps += 1
                cur_y -= distance
            elif direction == 'D':
                for y in range(cur_y, cur_y + distance):
                    path[(cur_x, y)].add(id)
                    path_steps[(cur_x, y)] = steps
                    steps += 1
                cur_y += distance
        return path_steps

    first_wire, second_wire = lines.split()
    first_wire_steps = parse_wire(first_wire, id='A')
    second_wire_steps = parse_wire(second_wire, id='B')

    return min(first_wire_steps[k] + second_wire_steps[k] for k, v in path.items() if len(v) > 1 and k != (0, 0))


assert calculate("R8,U5,L5,D3\nU7,R6,D4,L4\n") == 30
assert calculate("R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83") == 610
assert calculate("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7") == 410
