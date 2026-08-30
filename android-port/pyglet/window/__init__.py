"""pyglet.window, reduced to the key and mouse symbol tables.

The window, its event loop and touch input are not here yet; the game's
Cython modules import pyglet.window.key at their own import time purely to
read constants, and that has to work long before anything is drawn.
"""

from pyglet.window import key, mouse  # noqa: F401  (re-exported)
