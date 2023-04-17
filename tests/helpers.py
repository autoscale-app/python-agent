from contextlib import contextmanager
from datetime import timedelta
from freezegun import freeze_time

PLATFORM = "render"
TOKEN = "u4quBFgM72qun74EwashWv6Ll5TzhBVktVmicoWoXla"

time_unit_mapping = {
    'nanosecond': 'nanoseconds',
    'microsecond': 'microseconds',
    'millisecond': 'milliseconds',
    'second': 'seconds',
    'minute': 'minutes',
    'hour': 'hours',
    'day': 'days',
    'week': 'weeks',
    'month': 'months',
    'year': 'years',
}

@contextmanager
def travel(n, unit='second'):
    if unit not in time_unit_mapping:
        raise ValueError(f"Invalid time unit. Allowed units: {', '.join(time_unit_mapping.keys())}")

    with freeze_time() as frozen_time:
        frozen_time.tick(timedelta(**{time_unit_mapping[unit]: n}))
        yield
