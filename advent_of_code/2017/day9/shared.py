from typing import Union, List, Optional

GroupOrGarbage = Union['Group', 'Garbage']


class Group(object):
    def __init__(self):
        self.children: List[GroupOrGarbage] = []


class Garbage(object):
    def __init__(self, length: int):
        self.length = length


MODE_NORMAL = 'normal'
MODE_GARBAGE = 'garbage'
MODE_DONE = 'done'


def parse(text: str) -> GroupOrGarbage:
    mode: str = MODE_NORMAL
    ignore_next: bool = False
    garbage_length: int = 0
    stack: List[Group] = []
    last_value: Optional[GroupOrGarbage] = None

    for position, char in enumerate(text):
        if ignore_next and mode == MODE_GARBAGE:
            # reset the ignore flag
            ignore_next = False
            # and consume the character
        elif char == '{' and mode == MODE_NORMAL:
            # add an empty group to the stack
            stack.append(Group())

            # reset last_value
            last_value = None
        elif char == ',' and mode == MODE_NORMAL:
            assert len(stack) > 0, "Found comma without any opening brace"
            assert last_value is not None, "Found comma right after opening brace"

            # add last_value to the current group
            stack[-1].children.append(last_value)

            # consume last_value
            last_value = None
        elif char == '}' and mode == MODE_NORMAL:
            assert len(stack) > 0, "Found ending brace without any opening one"

            # add last_value to the current group
            if last_value is not None:
                stack[-1].children.append(last_value)

            # pop current group from the stack
            last_value = stack.pop()

            if len(stack) == 0:
                # we're at EOF
                mode = MODE_DONE
        elif char == '<' and mode == MODE_NORMAL:
            # set mode to garbage
            mode = MODE_GARBAGE

            # reset last_value
            last_value = None
            # and garbage length
            garbage_length = 0
        elif char == '>' and mode == MODE_GARBAGE:
            # reset mode to normal
            mode = MODE_NORMAL

            # and emit garbage
            last_value = Garbage(garbage_length)
        elif char == '!' and mode == MODE_GARBAGE:
            ignore_next = True
        elif mode == MODE_GARBAGE:
            # consume character
            garbage_length += 1
        else:
            raise ValueError(f"Invalid token '{char}' at position {position} (mode={mode})")

    return last_value


if __name__ == "__main__":
    GARBAGE_LINES = ('<>', '<random characters>', '<<<<>', '<{!>}>', '<!!>', '<!!!>>', '<{o"i!a,<{i<a>')
    for line in GARBAGE_LINES:
        assert isinstance(parse(line), Garbage)

    GROUPS = {
        '{}': 1,
        '{{{}}}': 3,
        '{{},{}}': 3,
        '{{{},{},{{}}}}': 6,
        '{<{},{},{{}}>}': 1,
        '{<a>,<a>,<a>,<a>}': 1,
        '{{<a>},{<a>},{<a>},{<a>}}': 5,
        '{{<!>},{<!>},{<!>},{<a>}}': 2,
    }

    def count_groups(group: Group) -> int:
        return 1 + sum(count_groups(child) for child in group.children if isinstance(child, Group))

    for line, group_count in GROUPS.items():
        res = parse(line)
        assert isinstance(res, Group)
        assert count_groups(res) == group_count
