import re
from datetime import datetime, timedelta
from typing import NamedTuple, List, Iterable

RE_LOG_RECORD = re.compile(r'^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)$')
RE_BEGINS_SHIFT = re.compile(r'^Guard #(\d+) begins shift$')


class TimeRange(NamedTuple):
    start: datetime
    end: datetime

    def __iter__(self) -> Iterable[datetime]:
        minutes = int((self.end - self.start).total_seconds() / 60)
        for i in range(minutes):
            yield self.start + timedelta(minutes=i)


class GuardShift(NamedTuple):
    guard_id: int
    start: datetime
    naps: List[TimeRange]

    @property
    def total_minutes_asleep(self):
        total_seconds = 0
        for nap in self.naps:
            total_seconds += (nap.end - nap.start).total_seconds()
        return total_seconds // 60


def parse_logs(text: str) -> Iterable[GuardShift]:
    # parse logs and order chronologically
    ordered_logs = []
    for line in text.splitlines():
        m = RE_LOG_RECORD.match(line)
        if m:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            hour = int(m.group(4))
            minute = int(m.group(5))
            current_timestamp = datetime(year, month, day, hour, minute)
            msg = m.group(6)

            ordered_logs.append((current_timestamp, msg))
    ordered_logs = sorted(ordered_logs, key=lambda x: x[0])

    last_timestamp = None
    current_guard = None
    for current_timestamp, msg in ordered_logs:
        if msg == 'falls asleep':
            assert current_guard is not None
        elif msg == 'wakes up':
            assert current_guard is not None
            current_guard.naps.append(
                TimeRange(
                    start=last_timestamp,
                    end=current_timestamp
                )
            )
        elif RE_BEGINS_SHIFT.match(msg):
            m = RE_BEGINS_SHIFT.match(msg)
            assert m is not None
            if current_guard is not None:
                yield current_guard
            current_guard = GuardShift(
                guard_id=int(m.group(1)),
                start=current_timestamp,
                naps=list()
            )

        last_timestamp = current_timestamp

    yield current_guard
