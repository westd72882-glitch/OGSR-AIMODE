"""Toolchain smoke test for the Android port.

Verifies that python-for-android can build and run an APK carrying the
dependencies the real port needs: Cython-compiled extensions, numpy and
an SDL2/GL ES surface. Replaced by the game entry point once the
toolchain is proven.
"""
import os
import sys

from kivy.app import App
from kivy.uix.label import Label


def _report():
    lines = ['toolchain check', '', 'python %d.%d.%d' % sys.version_info[:3]]

    for name in ('numpy', 'PIL', 'nbtlib'):
        try:
            mod = __import__(name)
            lines.append('%s %s OK' % (name, getattr(mod, '__version__', '')))
        except Exception as exc:
            lines.append('%s FAILED: %s' % (name, exc))

    try:
        from kivy.graphics.opengl import glGetString, GL_VERSION, GL_RENDERER
        lines.append('GL %s' % glGetString(GL_VERSION))
        lines.append('GPU %s' % glGetString(GL_RENDERER))
    except Exception as exc:
        lines.append('GL FAILED: %s' % exc)

    lines.append('abi %s' % os.environ.get('ANDROID_ARCH', 'n/a'))
    return '\n'.join(lines)


class ToolchainApp(App):
    def build(self):
        return Label(text=_report(), halign='center')


if __name__ == '__main__':
    ToolchainApp().run()
