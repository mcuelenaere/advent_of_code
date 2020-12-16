from collections import defaultdict

from .shared import parse_logs


def calculate(text: str) -> int:
    shifts = tuple(parse_logs(text))

    # determine minute when guard was most asleep
    asleep_minutes = defaultdict(lambda: 0)
    for shift in shifts:
        for nap in shift.naps:
            for time in nap:
                asleep_minutes[(shift.guard_id, time.minute)] += 1

    return next(
        guard_id * minute
        for (guard_id, minute), count in asleep_minutes.items()
        if count == max(asleep_minutes.values())
    )


puzzle = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""".strip()
assert calculate(puzzle) == 4455
