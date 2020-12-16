from typing import Iterable, List, Set


def parse_answer_groups(text: str) -> Iterable[List[Set[str]]]:
    current_group = []
    for line in text.splitlines():
        if line == "":
            yield current_group
            current_group = []
            continue

        answers = set(line)
        current_group.append(answers)

    if len(current_group) > 0:
        yield current_group
