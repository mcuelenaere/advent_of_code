from ..day05.shared import parse_instructions, streaming_evaluate
from itertools import combinations
import re


def parse_text(text: str):
    # ensure this only contains text for 1 room
    assert text.count("==") == 2

    lines = text.splitlines()

    name = next(line for line in lines if line.startswith("=="))[3:-3]

    try:
        index = lines.index("Doors here lead:")
    except ValueError:
        index = None
    if index is not None:
        end_index = lines.index("", index)
        doors = tuple(line[2:] for line in lines[index+1:end_index])
    else:
        doors = tuple()

    try:
        index = lines.index("Items here:")
    except ValueError:
        index = None
    if index is not None:
        end_index = lines.index("", index)
        items = tuple(line[2:] for line in lines[index+1:end_index])
    else:
        items = tuple()

    return name, doors, items


def calculate(text: str) -> str:
    inverse_direction = {
        'north': 'south',
        'south': 'north',
        'east': 'west',
        'west': 'east',
    }
    blacklisted_items = {'infinite loop', 'molten lava', 'giant electromagnet', 'escape pod', 'photons'}

    instructions = parse_instructions(text)
    gen = streaming_evaluate(instructions)

    def send(text: str):
        for c in text:
            gen.send(ord(c))
        gen.send(ord("\n"))

    def read():
        buf = ''
        c = next(gen)
        buf += chr(c)
        while c is not None:
            try:
                c = next(gen)
            except StopIteration:
                break
            if c is not None:
                buf += chr(c)
        return buf

    # discover all rooms
    stack = []
    inventory = set()
    seen_rooms = set()
    while True:
        buf = read()
        name, doors, items = parse_text(buf)

        if name == 'Security Checkpoint':
            # we're at the final room, move to the next phase
            break

        # store room info
        seen_rooms.add(name)

        # take all available items
        for item in items:
            if item in blacklisted_items:
                continue

            inventory.add(item)
            send(f"take {item}")
            read()  # discard output

        # find a new room to move to
        moving = False
        for door in doors:
            send(door)
            other_name, _, _ = parse_text(read())
            send(inverse_direction[door])
            read()  # discard

            if other_name in seen_rooms:
                continue

            stack.append(inverse_direction[door])
            moving = True

            # move to the new room
            send(door)
            break

        if not moving:
            # backtrack
            door = stack.pop()

            # move to the previous room
            send(door)

    # drop all inventory
    for item in inventory:
        send(f"drop {item}")
        read()  # discard output

    # bruteforce all inventory combinations to enter the pressure sensitive room
    for i in range(1, len(inventory)):
        for c in combinations(inventory, r=i):
            # take the required items for this combination
            for item in c:
                send(f"take {item}")
                read()  # discard output

            # sanity check
            send("inv")
            buf = read()
            assert set(line[2:] for line in buf.splitlines() if line.startswith("- ")) == set(c)

            # try entring the pressure-sensitive floor
            send("north")
            buf = read()
            if "Alert! Droids on this ship are lighter" in buf:
                # too heavy!
                pass
            elif "Alert! Droids on this ship are heavier" in buf:
                # too light!
                pass
            else:
                # success! Extract number from string
                return re.search(r'by typing (\d+) on the keypad', buf).group(1)

            # drop items again
            for item in c:
                send(f"drop {item}")
                read()  # discard output
