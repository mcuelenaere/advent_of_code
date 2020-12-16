import json


def walk(item) -> int:
    if isinstance(item, int):
        return item
    elif isinstance(item, list):
        return sum(walk(x) for x in item)
    elif isinstance(item, dict):
        return sum(walk(x) for x in item.values())
    elif isinstance(item, str):
        return 0
    else:
        raise ValueError(f"Unknown type {type(item)}: {item}")


def calculate(text: str) -> int:
    item = json.loads(text)
    return walk(item)


assert calculate("""[1,2,3]""") == 6
assert calculate("""{"a":2,"b":4}""") == 6
assert calculate("""[[[3]]]""") == 3
assert calculate("""{"a":{"b":4},"c":-1}""") == 3
assert calculate("""{"a":[-1,1]}""") == 0
assert calculate("""[-1,{"a":1}]""") == 0
assert calculate("""[]""") == 0
assert calculate("""{}""") == 0
