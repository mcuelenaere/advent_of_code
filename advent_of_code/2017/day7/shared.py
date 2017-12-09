import re


RE_DISC_LINE = re.compile(r'(\w+) \((\d+)\)(?: -> ([\w, ]+))?')


def parse_lines(lines):
    for line in lines:
        m = RE_DISC_LINE.match(line)
        if m is not None:
            parent = m.group(1)
            weight = int(m.group(2))
            children = m.group(3).split(', ') if m.group(3) else []
            yield parent, weight, children


def find_root(lines):
    all_children = set()
    all_parents = set()
    for name, _, children in lines:
        all_parents.add(name)
        all_children |= set(children)
    for parent in all_parents:
        if parent not in all_children:
            return parent
