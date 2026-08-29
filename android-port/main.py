"""Toolchain and port-readiness check for the Android build.

Reports, on screen, what the device actually gives us: the GL profile
(which decides whether the game's fixed-function renderer can be kept),
whether the Cython modules built by the mcgame recipe import, and whether
the pyglet shim resolves. Replaced by the game entry point once these all
come back green.
"""

import sys

from kivy.app import App
from kivy.uix.label import Label


def _line(label, fn):
    try:
        return '%s: %s' % (label, fn())
    except Exception as exc:
        return '%s: FAIL %s: %s' % (label, type(exc).__name__, exc)


def _gl_info():
    from kivy.graphics.opengl import glGetString, GL_VERSION, GL_RENDERER
    version = glGetString(GL_VERSION)
    renderer = glGetString(GL_RENDERER)
    for value in (version, renderer):
        if isinstance(value, bytes):
            value = value.decode('utf-8', 'replace')
    return '%s | %s' % (version, renderer)


def _cython_module():
    # World is one of the 33 .pyx modules; if the recipe cythonised and
    # cross-compiled correctly this import resolves to a native .so.
    from mc.net.minecraft.game.level import World
    return getattr(World, '__file__', 'imported')


def _shim():
    from pyglet.window import key, mouse
    return 'key.W=%d mouse.LEFT=%d' % (key.W, mouse.LEFT)


def _report():
    lines = ['port readiness', '', 'python %d.%d.%d' % sys.version_info[:3]]

    for name in ('numpy', 'PIL', 'nbtlib'):
        lines.append(_line(name, lambda n=name: getattr(
            __import__(n), '__version__', 'imported')))

    lines.append(_line('GL', _gl_info))
    lines.append(_line('cython mc', _cython_module))
    lines.append(_line('pyglet shim', _shim))
    return '\n'.join(lines)


class PortCheckApp(App):
    def build(self):
        return Label(text=_report(), halign='center', font_size='13sp')


if __name__ == '__main__':
    PortCheckApp().run()
