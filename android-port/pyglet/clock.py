"""The clock the game's loop ticks.

pyglet's clock also drives scheduled callbacks, and the game schedules two
of them, so tick() runs anything that has come due rather than only
measuring elapsed time.
"""

import time

_last = None
_scheduled = []


def tick(poll=False):
    """Seconds since the previous tick, and run what is due."""
    global _last
    now = time.monotonic()
    delta = 0.0 if _last is None else now - _last
    _last = now

    if _scheduled:
        due = [entry for entry in _scheduled if entry[0] <= now]
        for entry in due:
            _scheduled.remove(entry)
        for _when, func, args, kwargs in due:
            func(delta, *args, **kwargs)
    return delta


def schedule_once(func, delay, *args, **kwargs):
    _scheduled.append((time.monotonic() + delay, func, args, kwargs))


def unschedule(func):
    for entry in list(_scheduled):
        if entry[1] is func:
            _scheduled.remove(entry)


def get_fps():
    return 0.0 if not _last else 60.0
