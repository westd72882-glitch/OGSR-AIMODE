"""python-for-android recipe that cross-compiles the game's Cython modules.

Buildozer packages app sources as plain files and never runs Cython over
them, so the 33 .pyx modules holding the world, renderer and entity code
would simply be missing at runtime. This recipe builds them for the target
ABI and installs the `mc` package into the app's site-packages instead.
"""

import glob
import os
from os.path import dirname, join

from pythonforandroid.logger import info, warning
from pythonforandroid.recipe import CythonRecipe, IncludedFilesBehaviour


class MCGameRecipe(IncludedFilesBehaviour, CythonRecipe):
    version = '20100223'
    name = 'mcgame'

    # Relative to this file: the directory holding setup.py and the package.
    src_filename = join(dirname(__file__), '..', '..', 'game')

    depends = ['python3', 'numpy', 'setuptools', 'pillow']

    # The .pyx sources cimport numpy, so cythonisation runs on the host
    # toolchain rather than through the target interpreter.
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)

        # Sharing the runner's numpy over PYTHONPATH does not work: its C
        # extension is built for a different CPython than hostpython3, which
        # fails with "No module named numpy._core._multiarray_umath". Instead
        # setup.py goes through mcgame_setup_compat, which needs no numpy
        # import at all - only the header directory, passed here.
        includes = self._numpy_includes(arch)
        if includes:
            env['MCGAME_NUMPY_INCLUDE'] = includes[0]
            env['CFLAGS'] = env.get('CFLAGS', '') + ''.join(
                ' -I' + path for path in includes)
            info('mcgame: numpy headers at %s' % ', '.join(includes))
        else:
            warning('mcgame: no numpy headers found; modules that cimport '
                    'numpy will fail to compile')

        return env

    # Written by numpy's build, absent from its source tree. A candidate
    # include directory without these is the unbuilt copy and must not be
    # passed to the compiler - it shadows the real one and the build dies
    # on "unknown type name 'npy_uint64'".
    GENERATED_HEADERS = ('_numpyconfig.h', '__multiarray_api.h')

    def _numpy_includes(self, arch):
        """Include directories of the numpy actually built for this ABI."""
        roots = [self.ctx.get_python_install_dir(arch.arch)]
        try:
            roots.append(self.get_recipe('numpy', self.ctx).get_build_dir(arch.arch))
        except Exception:
            pass

        candidates = []
        for root in roots:
            for pattern in ('numpy/_core/include', 'numpy/core/include',
                            '**/numpy/_core/include', '**/numpy/core/include'):
                candidates.extend(glob.glob(join(root, pattern), recursive=True))

        complete = [path for path in sorted(set(candidates))
                    if all(os.path.exists(join(path, 'numpy', header))
                           for header in self.GENERATED_HEADERS)]
        if complete:
            return complete

        warning('mcgame: no numpy include dir carries %s; falling back to '
                'every candidate' % ', '.join(self.GENERATED_HEADERS))
        return sorted(set(candidates))


recipe = MCGameRecipe()
