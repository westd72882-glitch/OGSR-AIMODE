"""pyglet.window over SDL2, enough for the game to run itself.

The game subclasses Window and drives its own loop - dispatch_events,
on_draw, flip - so nothing here owns a main loop or fights it for control.
It creates the GL ES context, starts gl4es on it, translates SDL events
into the pyglet events the game already handles, and draws the touch
overlay after each frame.

Touches become keys and relative mouse motion (see android_input), so the
game never learns it is running on a phone.
"""

import ctypes

from pyglet.window import _sdl, key, mouse  # noqa: F401  (key, mouse re-exported)

#: Kept so the game's `while self.running` loop can be broken from outside.
_windows = []


class Window:
    def __init__(self, width=854, height=480, caption='', resizable=False,
                 vsync=False, visible=True, fullscreen=False, **_ignored):
        _sdl.load()
        if _sdl.Init(_sdl.INIT_VIDEO | _sdl.INIT_EVENTS) != 0:
            raise RuntimeError('SDL_Init failed: %s' % _sdl.error())

        # gl4es translates GL 1.x onto GLES2, so ask for exactly that; a
        # desktop profile request would simply fail here.
        _sdl.GL_SetAttribute(_sdl.GL_CONTEXT_PROFILE_MASK,
                             _sdl.GL_CONTEXT_PROFILE_ES)
        _sdl.GL_SetAttribute(_sdl.GL_CONTEXT_MAJOR_VERSION, 2)
        _sdl.GL_SetAttribute(_sdl.GL_CONTEXT_MINOR_VERSION, 0)
        _sdl.GL_SetAttribute(_sdl.GL_DEPTH_SIZE, 24)
        _sdl.GL_SetAttribute(_sdl.GL_DOUBLEBUFFER, 1)

        flags = _sdl.WINDOW_OPENGL | _sdl.WINDOW_SHOWN | _sdl.WINDOW_RESIZABLE
        self._window = _sdl.CreateWindow(
            caption.encode('utf-8'), _sdl.WINDOWPOS_UNDEFINED,
            _sdl.WINDOWPOS_UNDEFINED, int(width), int(height), flags)
        if not self._window:
            raise RuntimeError('SDL_CreateWindow failed: %s' % _sdl.error())

        self._context = _sdl.GL_CreateContext(self._window)
        if not self._context:
            raise RuntimeError('SDL_GL_CreateContext failed: %s' % _sdl.error())
        _sdl.GL_MakeCurrent(self._window, self._context)
        _sdl.GL_SetSwapInterval(1 if vsync else 0)

        # Android hands back the panel size, not the size that was asked
        # for, and the game reads self.width all over its layout code.
        self.width, self.height = self._query_size()

        from pyglet import gl
        gl.initialize(size=(self.width, self.height))

        self.has_exit = False
        self._handlers = []
        self._controls = self._make_controls()
        _windows.append(self)

    # -- SDL plumbing ------------------------------------------------------

    def _query_size(self):
        width, height = ctypes.c_int(0), ctypes.c_int(0)
        _sdl.GetWindowSize(self._window, ctypes.byref(width), ctypes.byref(height))
        return (width.value or 1), (height.value or 1)

    def _make_controls(self):
        from android_input import TouchControls

        return TouchControls(
            self.width, self.height,
            on_key=self._synth_key,
            on_button=self._synth_button,
            on_look=self._synth_look)

    # -- event synthesis ---------------------------------------------------

    def _synth_key(self, symbol, pressed):
        self.dispatch_event('on_key_press' if pressed else 'on_key_release',
                            symbol, 0)

    def _synth_button(self, button, pressed):
        # The game asks where the pointer is when a block is clicked, and
        # for a touch that is always the middle of the view: the crosshair.
        x, y = self.width // 2, self.height // 2
        self.dispatch_event('on_mouse_press' if pressed else 'on_mouse_release',
                            x, y, button, 0)

    def _synth_look(self, dx, dy):
        self.dispatch_event('on_mouse_motion', self.width // 2,
                            self.height // 2, dx, dy)

    # -- pyglet's event protocol ------------------------------------------

    def push_handlers(self, *handlers):
        self._handlers.extend(handlers)

    def event(self, handler):
        setattr(self, handler.__name__, handler)
        return handler

    def dispatch_event(self, name, *args):
        """Pushed handlers first, then the window's own method.

        pyglet stops at the first handler returning True; the game relies
        on that for its KeyStateHandler, which records a key and declines
        to consume it.
        """
        for handler in reversed(self._handlers):
            method = getattr(handler, name, None)
            if method is not None and method(*args):
                return True
        own = getattr(self, name, None)
        if own is not None:
            return bool(own(*args))
        return False

    def dispatch_events(self):
        buffer = (ctypes.c_ubyte * _sdl.EVENT_SIZE)()
        while _sdl.PollEvent(ctypes.byref(buffer)):
            self._handle(buffer)

    def _handle(self, buffer):
        kind = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_uint32))[0]

        if kind == _sdl.QUIT:
            self.has_exit = True
            self.dispatch_event('on_close')
            return

        if kind in (_sdl.FINGERDOWN, _sdl.FINGERUP, _sdl.FINGERMOTION):
            event = ctypes.cast(buffer,
                                ctypes.POINTER(_sdl.TouchFingerEvent))[0]
            # SDL reports normalised coordinates with y growing downwards;
            # the game, like pyglet, measures y from the bottom.
            x = event.x * self.width
            y = (1.0 - event.y) * self.height
            dx = event.dx * self.width
            dy = -event.dy * self.height
            if kind == _sdl.FINGERDOWN:
                self._controls.finger_down(event.fingerId, x, y)
            elif kind == _sdl.FINGERMOTION:
                self._controls.finger_move(event.fingerId, x, y, dx, dy)
            else:
                self._controls.finger_up(event.fingerId, x, y)
            return

        if kind == _sdl.WINDOWEVENT:
            event = ctypes.cast(buffer, ctypes.POINTER(_sdl.WindowEvent))[0]
            if event.event in (_sdl.WINDOWEVENT_RESIZED,
                               _sdl.WINDOWEVENT_SIZE_CHANGED):
                self.width, self.height = self._query_size()
                self._controls.resize(self.width, self.height)
                self.dispatch_event('on_resize', self.width, self.height)
            elif event.event == _sdl.WINDOWEVENT_FOCUS_GAINED:
                self.dispatch_event('on_activate')
            elif event.event == _sdl.WINDOWEVENT_FOCUS_LOST:
                self.dispatch_event('on_deactivate')

    # -- frame -------------------------------------------------------------

    def flip(self):
        try:
            self._controls.draw()
        except Exception:
            # A broken overlay must not cost the frame, or the game.
            pass
        _sdl.GL_SwapWindow(self._window)

    def clear(self):
        from pyglet import gl
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    # -- what a desktop window does and a phone cannot ---------------------

    def set_fullscreen(self, fullscreen=True):
        """Android is always fullscreen; the size never changes for this."""

    def set_exclusive_mouse(self, exclusive=True):
        """There is no cursor to capture."""

    def set_visible(self, visible=True):
        """The surface is on screen from the moment SDL creates it."""

    def set_mouse_position(self, x, y):
        """The game recentres the pointer after reading it; touches are
        already reported as deltas, so there is nothing to recentre."""

    def set_location(self, x, y):
        """A window on a phone has no location."""

    def set_icon(self, *images):
        """The launcher icon comes from the APK, not from the process."""

    def set_caption(self, caption):
        """Nothing displays a title here."""

    def activate(self):
        pass

    def close(self):
        self.has_exit = True

    def destroy(self):
        if self._window:
            _sdl.DestroyWindow(self._window)
            self._window = None
        if self in _windows:
            _windows.remove(self)

    # -- default handlers, so dispatch_event always finds something --------

    def on_draw(self):
        pass

    def on_resize(self, width, height):
        pass

    def on_close(self):
        self.has_exit = True
