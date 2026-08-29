"""Lets setup.py run under python-for-android's hostpython3.

hostpython3 is a bare interpreter built by p4a; it has neither numpy nor
Cython, while setup.py imports both at module level. It does not actually
need them: p4a cythonises every .pyx with the *runner's* Python before
calling setup.py, so the .c sources already exist by then, and the only
thing still wanted from numpy is its header directory, which the mcgame
recipe passes in through the environment.

On a host that does have both, this defers to the real ones.
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

try:
    from Cython.Build import cythonize as _real_cythonize
except ImportError:
    _real_cythonize = None


def cythonize(extensions, **kwargs):
    if _real_cythonize is not None:
        return _real_cythonize(extensions, **kwargs)

    # No Cython here: point each extension at the .c file p4a generated.
    for extension in extensions:
        extension.sources = [
            source[:-len('.pyx')] + '.c' if source.endswith('.pyx') else source
            for source in extension.sources
        ]
    return extensions
