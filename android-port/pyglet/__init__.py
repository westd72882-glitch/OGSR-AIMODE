"""Minimal stand-in for the pyglet package.

The game imports pyglet in 49 places. Rather than patch every one, this
package answers to the same name and provides only what the game actually
touches - which, off the gl and window submodules, is very little.
"""

import sys

#: pyglet lets an application switch options before the first window; the
#: game sets options['debug_gl'] and nothing here reads it back.
options = {
    'debug_gl': False,
    'audio': ('openal', 'silent'),
}

#: pyglet reports the platform it adapted itself to. Android's Python calls
#: itself linux, and the game branches on that in SoundManager, so report
#: it truthfully and let the audio shim decide what it can serve.
compat_platform = sys.platform

version = '1.5.31-android-shim'
