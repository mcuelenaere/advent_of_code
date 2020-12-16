import re

from typing import Dict, Iterable, Set


RE_PIPE_CONFIGURATION = re.compile(r"^(\d+) <-> ([\d,\s]+)$")

Configuration = Dict[int, Set[int]]


def parse_text(text: str) -> Configuration:
    configuration = dict()
    for line in text.splitlines():
        m = RE_PIPE_CONFIGURATION.match(line)
        if m is None:
            raise ValueError(f'Could not parse line "{line}"')
        left = int(m.group(1))
        right = set(map(int, m.group(2).split(", ")))
        configuration[left] = right
    return configuration


def find_connected_programs(config: Configuration, program: int) -> Iterable[int]:
    already_visited = set()

    def dfs(cur: int):
        if cur in already_visited:
            return
        else:
            already_visited.add(cur)

        for p in config[cur]:
            yield from dfs(p)
        yield cur

    yield from dfs(program)


def find_groups(config: Configuration) -> Iterable[Set[int]]:
    already_seen = set()
    for program in config.keys():
        if program in already_seen:
            continue

        group = set(find_connected_programs(config, program))
        yield group
        already_seen.update(group)
