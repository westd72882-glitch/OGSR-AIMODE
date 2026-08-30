"""Touch controls, in the game's own input vocabulary.

The game is a desktop program: it reads held keys through
pyglet.window.key and turns relative mouse motion into camera movement.
So rather than teach it about touches, this turns touches into exactly
those events. Nothing here knows about a UI toolkit - it takes finger
positions in window pixels and calls back - which is what lets the same
logic drive the game and be drawn over its frame.

    +---------------------------+---------------------------+
    |                           |         [ESC]  [E]        |
    |    move: virtual stick    |    look: drag anywhere    |
    |    (appears where you     |    tap: break block       |
    |     put your thumb)       |    hold: place block      |
    |         (O)               |                  (JUMP)   |
    +---------------------------+---------------------------+
"""

import time

from pyglet.window import key, mouse

#: Fractions of the shorter screen edge, so the controls stay thumb-sized
#: whatever the panel: the reporting device is 2000 px wide, and a thumb is
#: not.
STICK_RANGE = 0.20
STICK_DEADZONE = 0.045
BUTTON_SIZE = 0.20
BUTTON_MARGIN = 0.05

#: A press on the look side that is short and barely moved is a tap (break
#: a block); longer is a hold (place one).
TAP_SECONDS = 0.28
TAP_SLOP = 0.06

#: Touch travel to camera degrees. Tuned to feel like a mouse rather than
#: to match it: a finger crosses far less distance than a mouse does.
LOOK_SENSITIVITY = 1.6


class TouchControls:
    """Converts finger movement into key symbols, buttons and look deltas.

    `on_key` receives pyglet key symbols, `on_button` pyglet mouse buttons
    and `on_look` a relative delta shaped like on_mouse_motion's.
    """

    BUTTONS = (('jump', key.SPACE), ('inventory', key.E), ('escape', key.ESCAPE))

    DIRECTIONS = ((key.W, 0, 1), (key.S, 0, -1), (key.A, -1, 0), (key.D, 1, 0))

    def __init__(self, width, height, on_key=None, on_button=None, on_look=None):
        self.resize(width, height)
        self.on_key = on_key or (lambda symbol, pressed: None)
        self.on_button = on_button or (lambda button, pressed: None)
        self.on_look = on_look or (lambda dx, dy: None)

        self.held = set()
        self._fingers = {}
        self._stick_origin = None
        self._stick_thumb = None

    def resize(self, width, height):
        self.width = float(width)
        self.height = float(height)
        unit = min(self.width, self.height)
        self.stick_range = unit * STICK_RANGE
        self.stick_deadzone = unit * STICK_DEADZONE
        self.button_size = unit * BUTTON_SIZE
        self.button_margin = unit * BUTTON_MARGIN
        self.tap_slop = unit * TAP_SLOP

    # -- layout ------------------------------------------------------------

    def button_rects(self):
        """(name, symbol, x, y, size), y measured from the bottom."""
        size = self.button_size
        right = self.width - self.button_margin - size
        top = self.height - self.button_margin - size
        return (
            ('jump', key.SPACE, right, self.button_margin, size),
            ('inventory', key.E, right, top, size),
            ('escape', key.ESCAPE, right - size * 1.25, top, size * 0.8),
        )

    def _button_at(self, x, y):
        for name, symbol, bx, by, size in self.button_rects():
            if bx <= x <= bx + size and by <= y <= by + size:
                return symbol
        return None

    def _resting_stick(self):
        offset = self.stick_range + self.button_margin
        return (offset, offset)

    # -- input -------------------------------------------------------------

    def finger_down(self, finger, x, y):
        symbol = self._button_at(x, y)
        if symbol is not None:
            self._fingers[finger] = ('button', symbol)
            self._press(symbol, True)
            return

        if x < self.width * 0.5:
            self._fingers[finger] = ('move', None)
            self._stick_origin = (x, y)
            self._stick_thumb = (x, y)
            return

        self._fingers[finger] = ('look', {'time': time.monotonic(), 'moved': 0.0})

    def finger_move(self, finger, x, y, dx, dy):
        role, extra = self._fingers.get(finger, (None, None))
        if role == 'move':
            self._stick_thumb = (x, y)
            self._update_stick()
        elif role == 'look':
            extra['moved'] += abs(dx) + abs(dy)
            # The game moves the camera from a relative delta, exactly as a
            # mouse reports it, so no absolute position is involved.
            self.on_look(dx * LOOK_SENSITIVITY, dy * LOOK_SENSITIVITY)

    def finger_up(self, finger, x, y):
        role, extra = self._fingers.pop(finger, (None, None))
        if role == 'move':
            self._stick_origin = self._stick_thumb = None
            self._release_directions()
        elif role == 'button':
            self._press(extra, False)
        elif role == 'look':
            held = time.monotonic() - extra['time']
            if extra['moved'] < self.tap_slop:
                # A quick tap breaks a block, a deliberate hold places one -
                # the two mouse buttons a desktop player would use.
                button = mouse.LEFT if held < TAP_SECONDS else mouse.RIGHT
                self.on_button(button, True)
                self.on_button(button, False)

    def _press(self, symbol, pressed):
        if pressed:
            self.held.add(symbol)
        else:
            self.held.discard(symbol)
        self.on_key(symbol, pressed)

    def _release_directions(self):
        for symbol, _ax, _ay in self.DIRECTIONS:
            if symbol in self.held:
                self._press(symbol, False)

    def _update_stick(self):
        dx = self._stick_thumb[0] - self._stick_origin[0]
        dy = self._stick_thumb[1] - self._stick_origin[1]
        if (dx * dx + dy * dy) ** 0.5 < self.stick_deadzone:
            self._release_directions()
            return

        # Test each axis separately rather than picking one dominant
        # direction: walking north-east is the normal case, not an edge one.
        for symbol, ax, ay in self.DIRECTIONS:
            wanted = (dx * ax + dy * ay) > self.stick_deadzone * 0.7
            if wanted and symbol not in self.held:
                self._press(symbol, True)
            elif not wanted and symbol in self.held:
                self._press(symbol, False)

    # -- drawing -----------------------------------------------------------

    def draw(self):
        """Paint the overlay over whatever the game just rendered.

        Fixed-function GL, drawn straight after the game's frame and before
        the buffer swap, so the controls neither depend on the game's
        renderer nor disturb it: every piece of state touched is pushed and
        popped around the drawing.
        """
        from pyglet import gl

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0.0, self.width, 0.0, self.height, -1.0, 1.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_ALPHA_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        origin = self._stick_origin or self._resting_stick()
        self._ring(origin[0], origin[1], self.stick_range)

        thumb = self._stick_thumb or origin
        self._disc(thumb[0], thumb[1], self.stick_range * 0.42,
                   0.45 if self._stick_thumb else 0.22)

        for _name, symbol, bx, by, size in self.button_rects():
            self._quad(bx, by, size, size,
                       0.42 if symbol in self.held else 0.16)

        gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()

    # A ring, a disc and a quad are the whole vocabulary. Client-side
    # arrays rather than immediate mode: it is what the game uses, so it is
    # the path through gl4es that is already known to work.
    @staticmethod
    def _vertices(points, mode, alpha):
        import ctypes

        from pyglet import gl

        flat = [coordinate for point in points for coordinate in point]
        buffer = (gl.GLfloat * len(flat))(*flat)
        gl.glColor4f(1.0, 1.0, 1.0, alpha)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glVertexPointer(2, gl.GL_FLOAT, 0,
                           ctypes.cast(buffer, ctypes.c_void_p))
        gl.glDrawArrays(mode, 0, len(points))
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

    @staticmethod
    def _circle_points(cx, cy, radius, segments=28):
        import math
        step = 2.0 * math.pi / segments
        return [(cx + math.cos(i * step) * radius,
                 cy + math.sin(i * step) * radius) for i in range(segments)]

    def _quad(self, x, y, width, height, alpha):
        from pyglet import gl
        self._vertices([(x, y), (x + width, y),
                        (x + width, y + height), (x, y + height)],
                       gl.GL_QUADS, alpha)

    def _disc(self, cx, cy, radius, alpha):
        from pyglet import gl
        self._vertices([(cx, cy)] + self._circle_points(cx, cy, radius)
                       + [(cx + radius, cy)], gl.GL_TRIANGLE_FAN, alpha)

    def _ring(self, cx, cy, radius):
        from pyglet import gl
        self._vertices(self._circle_points(cx, cy, radius),
                       gl.GL_LINE_LOOP, 0.20)
