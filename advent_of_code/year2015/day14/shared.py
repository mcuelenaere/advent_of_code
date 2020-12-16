import re

from collections import Counter
from typing import Dict, NamedTuple


RE_LINE = re.compile(r"^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.$")
ReindeerProperties = NamedTuple("ReindeerProperties", fly_speed=int, fly_time=int, rest_time=int)


def parse_text(text: str) -> Dict[str, ReindeerProperties]:
    config = {}
    for line in text.splitlines():
        m = RE_LINE.match(line)
        if not m:
            raise ValueError(f'Could not parse line "{line}"')

        name, speed, fly_time, rest_time = m.groups()
        config[name] = ReindeerProperties(fly_speed=int(speed), fly_time=int(fly_time), rest_time=int(rest_time))
    return config


def calculate_distance_for(props: ReindeerProperties, timestamp: int) -> int:
    iteration_distance = props.fly_speed * props.fly_time
    iteration_length = props.fly_time + props.rest_time
    number_of_full_iterations, incomplete_iteration_duration = divmod(timestamp, iteration_length)
    return (
        number_of_full_iterations * iteration_distance
        + min(incomplete_iteration_duration, props.fly_time) * props.fly_speed
    )


def calculate_score(reindeers: Dict[str, ReindeerProperties], duration: int) -> int:
    scores = Counter()
    for timestamp in range(1, duration + 1):
        current_distances = {name: calculate_distance_for(props, timestamp) for name, props in reindeers.items()}
        max_distance = max(current_distances.values())
        scores.update({name: 1 if current_distances[name] == max_distance else 0 for name in reindeers.keys()})
    return max(scores.values())
