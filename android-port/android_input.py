"""Touch controls that speak the game's own input vocabulary.

The game is a desktop program: it reads the keyboard through
pyglet.window.key and turns the mouse into camera movement. Rather than
teach it about touches, this widget converts touches into exactly those
events - key symbols from pyglet's table, mouse buttons, and relative
motion - so it can later be wired into the window shim without the game
knowing a phone is involved.

Layout follows the two-thumb convention every mobile shooter uses:

    +---------------------------+---------------------------+
    |                           |          [ESC] [E]        |
    |                           |                           |
    |     move: virtual stick   |    look: drag anywhere    |
    |                           |    tap: break block       |
    |                           |    hold: place block      |
    |        (O)                |                  (JUMP)   |
    +---------------------------+---------------------------+

Sizes are in dp, not pixels: the reporting device is 2000 px wide, and a
thumb is the same size on every one of them.
"""

from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from pyglet.window import key, mouse

#: How far the thumb must travel from where it landed before a direction
#: counts as held. Below this the stick is centred and nothing is pressed.
STICK_DEADZONE = dp(14)

#: Travel at which the stick is fully deflected; also the ring's radius.
STICK_RANGE = dp(64)

#: A press on the look side shorter than this, that barely moved, is a tap
#: (break block). Longer is a hold (place block).
TAP_SECONDS = 0.28
TAP_SLOP = dp(18)

BUTTON_SIZE = dp(64)
BUTTON_MARGIN = dp(18)


class TouchControls(Widget):
    """Turns touches into held keys, mouse buttons and look deltas.

    Register callbacks rather than reading state: `on_look` fires with a
    relative delta, which is what the game's on_mouse_motion expects, and
    holding a direction is exposed through `held_keys` the same way
    pyglet's KeyStateHandler exposes a keyboard.
    """

    def __init__(self, on_look=None, on_button=None, **kwargs):
        super().__init__(**kwargs)
        self.on_look = on_look or (lambda dx, dy: None)
        self.on_button = on_button or (lambda button, pressed: None)

        #: pyglet key symbols currently held, for a KeyStateHandler stand-in.
        self.held_keys = set()

        self._stick_origin = None
        self._stick_thumb = None

        # Drawn as widgets rather than canvas text: an unlabelled square is
        # not a control, it is a guess.
        self._captions = {}
        for name, caption in (('jump', 'JUMP'), ('inventory', 'E'),
                              ('escape', 'ESC')):
            label = Label(text=caption, font_size='13sp', size_hint=(None, None))
            self._captions[name] = label
            self.add_widget(label)

        self.bind(pos=self._redraw, size=self._redraw)

    # -- geometry ----------------------------------------------------------

    @property
    def _split(self):
        """x of the line between the move half and the look half."""
        return self.x + self.width * 0.5

    def _buttons(self):
        """Named tap targets, as (name, x, y, size) in window coordinates."""
        right = self.right - BUTTON_MARGIN
        top = self.top - BUTTON_MARGIN
        return (
            ('jump', right - BUTTON_SIZE, self.y + BUTTON_MARGIN, BUTTON_SIZE),
            ('inventory', right - BUTTON_SIZE, top - BUTTON_SIZE, BUTTON_SIZE),
            ('escape', right - BUTTON_SIZE * 2.2, top - BUTTON_SIZE,
             BUTTON_SIZE * 0.8),
        )

    def _button_at(self, x, y):
        for name, bx, by, size in self._buttons():
            if bx <= x <= bx + size and by <= y <= by + size:
                return name
        return None

    # -- touch handling ----------------------------------------------------

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False

        button = self._button_at(*touch.pos)
        if button:
            touch.ud['role'] = 'button'
            touch.ud['button'] = button
            self._press_button(button, True)
            self._redraw()
            return True

        if touch.x < self._split:
            touch.ud['role'] = 'move'
            self._stick_origin = touch.pos
            self._stick_thumb = touch.pos
            self._redraw()
            return True

        touch.ud['role'] = 'look'
        touch.ud['start'] = touch.pos
        touch.ud['time'] = touch.time_start
        touch.ud['moved'] = 0.0
        return True

    def on_touch_move(self, touch):
        role = touch.ud.get('role')
        if role == 'move':
            self._stick_thumb = touch.pos
            self._update_stick()
            self._redraw()
            return True
        if role == 'look':
            touch.ud['moved'] += abs(touch.dx) + abs(touch.dy)
            # The game moves the camera from a relative delta, so hand it
            # the same thing a mouse would report.
            self.on_look(touch.dx, touch.dy)
            return True
        return False

    def on_touch_up(self, touch):
        role = touch.ud.get('role')
        if role == 'move':
            self._stick_origin = self._stick_thumb = None
            self._release_directions()
            self._redraw()
            return True
        if role == 'button':
            self._press_button(touch.ud['button'], False)
            self._redraw()
            return True
        if role == 'look':
            held = touch.time_end - touch.ud['time']
            still = touch.ud['moved'] < TAP_SLOP
            if still:
                # A quick tap breaks a block, a deliberate hold places one:
                # the two mouse buttons a desktop player would use.
                button = mouse.LEFT if held < TAP_SECONDS else mouse.RIGHT
                self.on_button(button, True)
                self.on_button(button, False)
            return True
        return False

    # -- state -------------------------------------------------------------

    #: One place, because a caption, a highlight and a keypress that
    #: disagree about which button was hit is a bug waiting to happen.
    BUTTON_KEYS = {'jump': key.SPACE, 'inventory': key.E, 'escape': key.ESCAPE}

    def _press_button(self, name, pressed):
        symbol = self.BUTTON_KEYS[name]
        if pressed:
            self.held_keys.add(symbol)
        else:
            self.held_keys.discard(symbol)
        self.on_button(symbol, pressed)

    DIRECTIONS = ((key.W, 0, 1), (key.S, 0, -1), (key.A, -1, 0), (key.D, 1, 0))

    def _release_directions(self):
        for symbol, _dx, _dy in self.DIRECTIONS:
            self.held_keys.discard(symbol)

    def _update_stick(self):
        dx = self._stick_thumb[0] - self._stick_origin[0]
        dy = self._stick_thumb[1] - self._stick_origin[1]
        self._release_directions()
        if (dx * dx + dy * dy) ** 0.5 < STICK_DEADZONE:
            return
        # Diagonals matter - a player walks north-east constantly - so test
        # each axis separately instead of picking one dominant direction.
        for symbol, ax, ay in self.DIRECTIONS:
            projection = dx * ax + dy * ay
            if projection > STICK_DEADZONE * 0.7:
                self.held_keys.add(symbol)

    # -- drawing -----------------------------------------------------------

    def _redraw(self, *_args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 0.22)
            origin = self._stick_origin or (
                self.x + STICK_RANGE + BUTTON_MARGIN * 2,
                self.y + STICK_RANGE + BUTTON_MARGIN * 2)
            Line(circle=(origin[0], origin[1], STICK_RANGE), width=dp(1.5))

            thumb = self._stick_thumb or origin
            Color(1, 1, 1, 0.45 if self._stick_thumb else 0.25)
            radius = STICK_RANGE * 0.42
            Ellipse(pos=(thumb[0] - radius, thumb[1] - radius),
                    size=(radius * 2, radius * 2))

            for name, bx, by, size in self._buttons():
                symbol = self.BUTTON_KEYS[name]
                Color(1, 1, 1, 0.4 if symbol in self.held_keys else 0.18)
                Rectangle(pos=(bx, by), size=(size, size))

        for name, bx, by, size in self._buttons():
            caption = self._captions[name]
            caption.size = (size, size)
            caption.pos = (bx, by)
