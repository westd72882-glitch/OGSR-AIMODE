"""pyglet.app, reduced to the event-loop object the game starts and stops.

The game runs its own loop and only asks the platform loop to let the OS
breathe between frames. SDL's event pump already does that inside
Window.dispatch_events, so these are deliberately empty rather than
missing: the game calls them, and a stub that does nothing is correct here
rather than merely convenient.
"""


class _PlatformEventLoop:
    def start(self):
        pass

    def step(self, timeout=None):
        pass

    def stop(self):
        pass

    def notify(self):
        pass


platform_event_loop = _PlatformEventLoop()


def run():
    from pyglet.window import _windows
    for window in list(_windows):
        while not window.has_exit:
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()


def exit():
    from pyglet.window import _windows
    for window in _windows:
        window.has_exit = True
