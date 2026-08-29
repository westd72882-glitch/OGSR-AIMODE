"""python-for-android recipe that cross-compiles the game's Cython modules.

Buildozer packages app sources as plain files and never runs Cython over
them, so the 33 .pyx modules holding the world, renderer and entity code
would simply be missing at runtime. This recipe builds them for the target
ABI and installs the `mc` package into the app's site-packages instead.
"""

import glob
import os
import shutil
import sys
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

        # This recipe builds before p4a installs the recipe-less pure Python
        # requirements, so it is the last chance to fix the pip that step needs.
        self._repair_hostpython_pip()

    def _repair_hostpython_pip(self):
        """Reinstall pip inside hostpython3 when its own copy is unusable.

        The pip that ships in p4a's host interpreter is inconsistent here -
        importing it raises

            ImportError: cannot import name 'BuildDependencyInstallError'
                         from 'pip._internal.exceptions'

        and p4a needs a working one to install the pure-Python requirements
        that have no recipe (nbtlib, requests and friends). ensurepip
        bootstraps from a bundled wheel and does not import the installed
        pip, so it can replace a broken one - but only over a clean slate,
        hence removing the existing package first.
        """
        hostpython = sh.Command(self.ctx.hostpython)
        try:
            shprint(hostpython, '-c', 'import pip._internal.cli.main')
            return
        except Exception:
            info('mcgame: hostpython pip is broken, reinstalling it')

        root = dirname(dirname(str(self.ctx.hostpython)))
        for site in glob.glob(join(root, 'lib', 'python*', 'site-packages')):
            for leftover in glob.glob(join(site, 'pip')) + glob.glob(join(site, 'pip-*')):
                shutil.rmtree(leftover, ignore_errors=True)
                info('mcgame: removed %s' % leftover)

        shprint(hostpython, '-m', 'ensurepip', '--upgrade', '--default-pip')
        shprint(hostpython, '-c', 'import pip._internal.cli.main; print("pip repaired")')

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

        self._preinstall_pure_requirements(arch)

    # Pulled in transitively by kivy (via kivy-garden -> requests) and by
    # nbtlib. Every one of them is pure Python and ships a py3-none-any
    # wheel, but p4a hands them to pip with the Android cross-compiler set,
    # which builds wheels tagged android_24_arm64_v8a that the host pip then
    # refuses to install:
    #
    #   ERROR: charset_normalizer-...-android_24_arm64_v8a.whl is not a
    #   supported wheel on this platform.
    #
    # p4a skips any module already present in the target site-packages, so
    # placing the pure wheels there first avoids that path entirely.
    PURE_PYTHON_REQUIREMENTS = (
        'certifi', 'chardet', 'charset_normalizer', 'docutils', 'filetype',
        'idna', 'Kivy-Garden', 'nbtlib', 'pygments', 'requests', 'six',
        'urllib3',
    )

    def _preinstall_pure_requirements(self, arch):
        target = self.ctx.get_python_install_dir(arch.arch)
        info('mcgame: pre-installing pure Python requirements into %s' % target)
        shprint(
            sh.Command(sys.executable), '-m', 'pip', 'install',
            '--target', target, '--no-deps', '--upgrade',
            '--only-binary=:all:', '--platform', 'any',
            '--python-version', self.python_major_minor_version,
            '--implementation', 'py',
            *self.PURE_PYTHON_REQUIREMENTS
        )

        self._mark_present(target)

    def _mark_present(self, target):
        """Make p4a's presence check succeed for every requirement.

        p4a compares the *distribution* name against a path in site-packages,
        but a wheel unpacks under its import name and the two rarely agree on
        case or separator: Pygments installs as pygments, Kivy-Garden as
        kivy_garden. The check then never matches, the module stays in the
        list, and p4a builds the virtualenv whose pip is broken here.

        So leave an empty marker for whichever spelling is missing. None of
        them can shadow a real import: the genuine package is already there
        under its own name, and hyphenated names are not importable at all.
        """
        def variants(name):
            lowered = name.lower()
            return {name, lowered,
                    name.replace('-', '_'), lowered.replace('-', '_'),
                    name.replace('_', '-'), lowered.replace('_', '-')}

        for requirement in self.PURE_PYTHON_REQUIREMENTS:
            for spelling in sorted(variants(requirement)):
                if any(os.path.exists(join(target, spelling + suffix))
                       for suffix in ('', '.py', '.pyc', '.so')):
                    continue
                os.makedirs(join(target, spelling), exist_ok=True)
                info('mcgame: marked %s as present' % spelling)

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
