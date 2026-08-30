"""pyglet.canvas, used once: to centre a window on the desktop.

There is no desktop and nothing to centre, but the game reads screen
dimensions before deciding, so report the panel it is already filling.
"""


class Screen:
    def __init__(self, width, height):
        self.x = self.y = 0
        self.width = width
        self.height = height


class Display:
    def get_default_screen(self):
        from pyglet.window import _windows
        if _windows:
            return Screen(_windows[0].width, _windows[0].height)
        return Screen(1280, 720)

    def get_screens(self):
        return [self.get_default_screen()]

    def get_windows(self):
        from pyglet.window import _windows
        return list(_windows)
