"""python-for-android recipe that cross-compiles the game's Cython modules.

Buildozer packages app sources as plain files and never runs Cython over
them, so the 33 .pyx modules holding the world, renderer and entity code
would simply be missing at runtime. This recipe builds them for the target
ABI and installs the `mc` package into the app's site-packages instead.
"""

import glob
import os
import shutil
from os.path import dirname, isdir, join

import sh
from pythonforandroid.logger import info, shprint, warning
from pythonforandroid.recipe import CythonRecipe, IncludedFilesBehaviour
from pythonforandroid.util import current_directory


class MCGameRecipe(IncludedFilesBehaviour, CythonRecipe):
    version = '20100223'
    name = 'mcgame'

    # Relative to this file: the directory holding setup.py and the package.
    src_filename = join(dirname(__file__), '..', '..', 'game')

    depends = ['python3', 'numpy', 'setuptools', 'pillow']

    # Cythonisation runs on the build host rather than through the target
    # interpreter.
    call_hostpython_via_targetpython = False

    # Regenerate unconditionally. Cython skips a .pyx whose .c is newer, and
    # the build directory is restored from CI cache, so a .c left by an
    # earlier run with a different numpy would otherwise be compiled as-is.
    cython_args = ['-f']

    # Written by numpy's build, absent from its source tree. A candidate
    # include directory without these is the unbuilt copy and must not be
    # passed to the compiler - it shadows the real one and the build dies
    # on "unknown type name 'npy_uint64'".
    GENERATED_HEADERS = ('_numpyconfig.h', '__multiarray_api.h')

    def prebuild_arch(self, arch):
        """Drop generated C left over from a previous run."""
        super().prebuild_arch(arch)

        build_dir = self.get_build_dir(arch.arch)
        stale = glob.glob(join(build_dir, '**', '*.c'), recursive=True)
        for path in stale:
            os.remove(path)
        if stale:
            info('mcgame: removed %d stale generated C file(s)' % len(stale))

    def install_python_package(self, arch, name=None, env=None, is_dir=True):
        """Install the built package without pip.

        p4a installs with hostpython3's own pip, which in this environment
        is broken - importing it raises

            ImportError: cannot import name 'BuildDependencyInstallError'
                         from 'pip._internal.exceptions'

        Nothing here needs a package manager: run setup.py build, which puts
        the compiled extensions and the package data side by side under
        build/lib.*, and copy that tree into the app's site-packages.
        """
        if env is None:
            env = self.get_recipe_env(arch)

        build_dir = self.get_build_dir(arch.arch)
        with current_directory(build_dir):
            shprint(sh.Command(self.ctx.hostpython), 'setup.py', 'build', '-v',
                    _env=env, *self.setup_extra_args)

        staged = sorted(glob.glob(join(build_dir, 'build', 'lib.*')))
        if not staged:
            raise RuntimeError(
                'mcgame: setup.py build produced no build/lib.* directory')

        target = self.ctx.get_python_install_dir(arch.arch)
        info('mcgame: installing %s into %s' % (staged[-1], target))
        for entry in os.listdir(staged[-1]):
            source = join(staged[-1], entry)
            destination = join(target, entry)
            if isdir(source):
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                shutil.copy2(source, destination)

    def get_recipe_env(self, arch, **kwargs):
        env = super().get_recipe_env(arch, **kwargs)

        # Sharing the host's numpy over PYTHONPATH does not work - its C
        # extension targets a different CPython than hostpython3. setup.py
        # goes through mcgame_setup_compat instead and needs only the header
        # directory, passed here.
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
