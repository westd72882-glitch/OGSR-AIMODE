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

        # Cythonisation runs under hostpython3, which has no numpy of its
        # own, so `cimport numpy` fails there. p4a itself runs on the
        # runner's interpreter, which does have numpy, and both are x86_64
        # CPython - so point hostpython3 at that copy rather than trying to
        # install into it (it may have no pip).
        host_numpy = self._host_numpy_path()
        if host_numpy:
            env['PYTHONPATH'] = os.pathsep.join(
                [host_numpy] + [p for p in [env.get('PYTHONPATH')] if p])
            info('mcgame: hostpython numpy via PYTHONPATH=%s' % host_numpy)
        else:
            warning('mcgame: numpy not importable from the build host; '
                    'cimport numpy will fail')

        includes = self._numpy_includes(arch)
        if includes:
            env['CFLAGS'] = env.get('CFLAGS', '') + ''.join(
                ' -I' + path for path in includes)
            info('mcgame: numpy headers at %s' % ', '.join(includes))
        else:
            warning('mcgame: no numpy headers found; modules that cimport '
                    'numpy will fail to compile')

        return env

    def _host_numpy_path(self):
        """site-packages of the numpy that p4a itself imports, if any."""
        try:
            import numpy
        except ImportError:
            return None
        return dirname(dirname(numpy.__file__))

    def _numpy_includes(self, arch):
        """Locate the numpy headers built for this ABI.

        The directory moved from numpy/core to numpy/_core in numpy 2, and
        p4a stages it under either the install dir or the build dir
        depending on version, so probe for whichever exists.
        """
        roots = [self.ctx.get_python_install_dir(arch.arch)]
        try:
            roots.append(self.get_recipe('numpy', self.ctx).get_build_dir(arch.arch))
        except Exception:
            pass

        found = []
        for root in roots:
            for pattern in ('numpy/_core/include', 'numpy/core/include',
                            '**/numpy/_core/include', '**/numpy/core/include'):
                found.extend(glob.glob(join(root, pattern), recursive=True))
        return sorted(set(found))


recipe = MCGameRecipe()
