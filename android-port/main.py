"""Port-readiness probe for the Android build.

The first APK died on a black screen, which tells us nothing: on Android a
Python exception before the window exists, and a segfault inside a native
extension, look exactly the same from the outside. So this draws the
window first and only then runs the checks, one per frame, naming each
check on screen *before* running it. A hard crash therefore leaves the
name of the guilty probe visible on the last rendered frame.
"""

import os
import sys
import traceback

# Nothing here may import numpy, PIL or the game's native modules: at module
# level a failure means a black screen, and identifying it is the whole point.
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


def _log_path():
    """A file the user can actually reach with a file manager.

    An app's own directory under /sdcard/Android/data needs no permission
    and stays browsable, so if the window never appears the report is still
    recoverable. Falls back to the private directory, which at least keeps
    the code path identical.
    """
    package = 'org.mcpython.mcpython'
    try:
        from android.storage import primary_external_storage_path
        base = os.path.join(primary_external_storage_path(),
                            'Android', 'data', package, 'files')
        os.makedirs(base, exist_ok=True)
    except Exception:
        base = os.environ.get('ANDROID_PRIVATE') or os.getcwd()
    return os.path.join(base, 'port-check.txt')


def _probe_python():
    return '%d.%d.%d' % sys.version_info[:3]


def _probe_site():
    """List what actually landed in site-packages.

    The recipe leaves empty marker directories for distributions p4a would
    otherwise try to install itself; an empty one that shadows a real import
    name would break at runtime, so name the ones that are empty.
    """
    import site
    roots = [p for p in sys.path if p.endswith('site-packages')]
    roots += [p for p in getattr(site, 'getsitepackages', list)() if p not in roots]
    empty = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for entry in sorted(os.listdir(root)):
            path = os.path.join(root, entry)
            if os.path.isdir(path) and not os.listdir(path):
                empty.append(entry)
    return 'empty dirs: %s' % (', '.join(empty) if empty else 'none')


def _probe_gl():
    from kivy.graphics.opengl import GL_RENDERER, GL_VERSION, glGetString

    def text(value):
        return value.decode('utf-8', 'replace') if isinstance(value, bytes) else str(value)

    return '%s | %s' % (text(glGetString(GL_VERSION)),
                        text(glGetString(GL_RENDERER)))


def _probe_numpy():
    import numpy
    return '%s (%s)' % (numpy.__version__, numpy.zeros(3).sum())


def _probe_pil():
    import PIL
    from PIL import Image
    Image.new('RGB', (2, 2))
    return PIL.__version__


def _probe_nbtlib():
    import nbtlib
    return getattr(nbtlib, '__version__', 'imported')


def _probe_shim():
    from pyglet.window import key, mouse
    return 'key.W=%d mouse.LEFT=%d' % (key.W, mouse.LEFT)


def _probe_gl_binding():
    """Load the GL binding without calling into GL.

    Importing pyglet.gl only dlopens gl4es and resolves symbols, which is
    all the game's Cython modules need at their own import time - and is
    what the previous build crashed on.
    """
    from pyglet import gl
    return '%d entry points missing%s' % (
        len(gl.MISSING),
        (': ' + ', '.join(gl.MISSING[:6])) if gl.MISSING else '')


def _probe_gl4es():
    """Start gl4es and ask it what it is.

    Deliberately the last probe: gl4es takes over the GL state machine of
    the context it is initialised in, so Kivy may not draw another correct
    frame afterwards. By this point everything else is already on screen
    and in the log file.
    """
    from kivy.core.window import Window as _W
    from pyglet import gl
    gl.initialize(size=_W.size)
    return gl.gl_info.get_version()


def _probe_cython():
    # One of the 33 .pyx modules. Loads a native .so linked against numpy,
    # so this is the probe most likely to take the process down outright.
    from mc.net.minecraft.game.level import World
    return os.path.basename(getattr(World, '__file__', 'imported'))


def _probe_resources():
    from mc import Resources
    return '%d entries' % len(getattr(Resources, 'resources', {}) or {})


PROBES = (
    ('python', _probe_python),
    ('site-packages', _probe_site),
    ('GL', _probe_gl),
    ('numpy', _probe_numpy),
    ('pillow', _probe_pil),
    ('nbtlib', _probe_nbtlib),
    ('pyglet shim', _probe_shim),
    ('pyglet gl', _probe_gl_binding),
    ('cython mc', _probe_cython),
    ('game resources', _probe_resources),
    ('gl4es init', _probe_gl4es),
)


#: pyglet symbols read back as names, so the controls preview says "W"
#: rather than 119. Built lazily: importing the shim at module level would
#: put a GL binding in the way of the report it is meant to produce.
_KEY_NAMES = {}


def _load_key_names():
    from pyglet.window import key, mouse
    for name in dir(key):
        if not name.startswith('_') and isinstance(getattr(key, name), int):
            _KEY_NAMES.setdefault(getattr(key, name), name)
    _KEY_NAMES[mouse.LEFT] = 'BREAK'
    _KEY_NAMES[mouse.RIGHT] = 'PLACE'


class PortCheckApp(App):
    def build(self):
        Window.clearcolor = (0.06, 0.06, 0.08, 1)
        self.log_path = _log_path()
        self.lines = ['port readiness', 'log: %s' % self.log_path, '']
        self.label = Label(text='\n'.join(self.lines), font_size='13sp',
                           halign='left', valign='top', size_hint_y=None,
                           markup=False)
        self.label.bind(
            width=lambda *_: setattr(self.label, 'text_size',
                                     (self.label.width - 16, None)),
            texture_size=lambda *_: setattr(self.label, 'height',
                                            self.label.texture_size[1]))
        view = ScrollView()
        view.add_widget(self.label)

        # The report and the controls preview swap places inside this, so
        # neither has to know the other exists.
        self.container = FloatLayout()
        self.container.add_widget(view)
        self.root_view = self.container

        self.queue = list(PROBES)
        self.pending = None
        # One probe per tick, and only after the frame that announced it has
        # been drawn - otherwise a segfault erases the evidence.
        Clock.schedule_interval(self._step, 0.25)
        return self.container

    def _show(self):
        text = '\n'.join(self.lines)
        self.label.text = text
        # Rewritten after every step, so a crash still leaves everything up
        # to and including the probe that caused it.
        try:
            with open(self.log_path, 'w') as handle:
                handle.write(text + '\n')
        except Exception:
            pass

    def _step(self, _dt):
        if self.pending is not None:
            name, fn = self.pending
            self.pending = None
            try:
                self.lines[-1] = '%s: %s' % (name, fn())
            except BaseException:
                detail = traceback.format_exc().strip().splitlines()
                self.lines[-1] = '%s: FAIL\n    %s' % (
                    name, '\n    '.join(detail[-4:]))
            self._show()
            return True

        if not self.queue:
            self.lines.append('')
            self.lines.append('all probes finished - touch anywhere for controls')
            self._show()
            self._offer_controls()
            return False

        self.pending = self.queue.pop(0)
        self.lines.append('%s: running...' % self.pending[0])
        self._show()
        return True


    def _offer_controls(self):
        """Swap the report for the touch controls on the next touch.

        The control layer does not depend on the game loop, so it can be
        tried - and criticised - long before there is a world to walk
        around in. Reaching it costs one touch so the report stays
        readable until it has been read.
        """
        self.root_view.bind(on_touch_down=lambda *_: self._show_controls())

    def _show_controls(self):
        if getattr(self, '_controls_shown', False):
            return False
        self._controls_shown = True

        from android_input import TouchControls

        _load_key_names()

        readout = Label(text='move with the left half, look with the right',
                        font_size='14sp', size_hint=(1, None), height='40dp',
                        pos_hint={'top': 1})

        def describe():
            names = sorted(_KEY_NAMES.get(s, str(s)) for s in controls.held_keys)
            readout.text = 'held: %s   look: %+d %+d   last: %s' % (
                ', '.join(names) or '-', state['dx'], state['dy'],
                state['last'])

        state = {'dx': 0, 'dy': 0, 'last': '-'}

        def looked(dx, dy):
            state['dx'], state['dy'] = int(dx), int(dy)
            describe()

        def pressed(symbol, is_down):
            state['last'] = '%s %s' % (_KEY_NAMES.get(symbol, symbol),
                                       'down' if is_down else 'up')
            describe()

        controls = TouchControls(on_look=looked, on_button=pressed)
        layout = FloatLayout()
        layout.add_widget(controls)
        layout.add_widget(readout)

        self.container.clear_widgets()
        self.container.add_widget(layout)
        return True


if __name__ == '__main__':
    try:
        PortCheckApp().run()
    except BaseException:
        # Reaching here means Kivy itself gave up; the traceback is only
        # visible through logcat, but printing it costs nothing.
        traceback.print_exc()
        raise
