"""pyglet.resource, for the two things the game gets from it.

Every texture in this game is a Python literal in mc/Resources.py, not a
file, so the resource system is only asked for the window icon - which an
APK supplies itself - and for a writable directory.
"""

import os

#: The game appends to this before calling reindex().
path = ['.']


def reindex():
    """Nothing is indexed: there is no resource tree to walk."""


class _Icon:
    """Stands in for an image, because set_icon is a no-op on Android."""

    width = height = 0


def image(name, **_kwargs):
    return _Icon()


def get_script_home():
    return os.path.dirname(os.path.abspath(__file__))
