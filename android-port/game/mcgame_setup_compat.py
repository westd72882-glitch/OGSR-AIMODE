"""Lets setup.py run under python-for-android's hostpython3.

hostpython3 is a bare interpreter built by p4a; it has no numpy, while
setup.py imports it at module level purely for its header directory. The
mcgame recipe passes that directory in through the environment instead.

It does ship a Cython, but an old one that still bundles its own
numpy/__init__.pxd written for numpy 1, where the descriptor's subarray
field was public. Cythonising with it produces `d->subarray`, which does
not compile against numpy 2 headers. p4a runs its own cythonisation step
with the modern Cython on the build host, and its build sequence expects
the first setup.py invocation to fail for want of .c files - so this
never calls Cython at all and simply points each extension at the .c that
step produces.
"""

import os


class _NumpyStub:
    """Just enough of numpy for setup.py's include_dirs."""

    @staticmethod
    def get_include():
        return os.environ.get('MCGAME_NUMPY_INCLUDE', '')


try:
    import numpy
except ImportError:
    numpy = _NumpyStub()


def cythonize(extensions, **kwargs):
    """Map .pyx sources onto the .c files p4a generates. Never runs Cython."""
    for extension in extensions:
        extension.sources = [
            source[:-len('.pyx')] + '.c' if source.endswith('.pyx') else source
            for source in extension.sources
        ]
    return extensions
