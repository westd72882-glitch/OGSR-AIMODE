"""State handlers the game pushes onto the window.

pyglet keeps these in the key and mouse modules; they live apart here
because those two files are generated tables and this is behaviour.

Neither handler returns True: pyglet's do not either, and the game depends
on it - a key must be recorded *and* still reach the window's own
on_key_press, which is where the game acts on it.
"""


class KeyStateHandler(dict):
    """Reads like a keyboard: handler[key.W] is True while W is held."""

    def on_key_press(self, symbol, modifiers):
        self[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self[symbol] = False

    def __getitem__(self, symbol):
        return self.get(symbol, False)


class MouseStateHandler(dict):
    """The same, for mouse buttons, plus the last position pyglet reports."""

    def on_mouse_press(self, x, y, button, modifiers):
        self[button] = True

    def on_mouse_release(self, x, y, button, modifiers):
        self[button] = False

    def on_mouse_motion(self, x, y, dx, dy):
        self['x'], self['y'] = x, y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self['x'], self['y'] = x, y

    def __getitem__(self, name):
        return self.get(name, False)
