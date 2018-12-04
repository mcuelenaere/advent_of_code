from collections import defaultdict
from .shared import parse_logs


def calculate(text: str) -> int:
    shifts = tuple(parse_logs(text))

    # determine guard which was most asleep
    asleep_time = defaultdict(lambda: 0)
    for shift in shifts:
        asleep_time[shift.guard_id] += shift.total_minutes_asleep

    most_sleepy_guard = next(id for id, sleep_time in asleep_time.items() if sleep_time == max(asleep_time.values()))

    # determine minute when guard was most asleep
    asleep_minutes = defaultdict(lambda: 0)
    for shift in shifts:
        if shift.guard_id != most_sleepy_guard:
            continue

        for nap in shift.naps:
            for time in nap:
                asleep_minutes[time.minute] += 1

    most_sleepy_minute = next(minute for minute, count in asleep_minutes.items() if count == max(asleep_minutes.values()))

    return most_sleepy_guard * most_sleepy_minute


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
assert calculate(puzzle) == 240
