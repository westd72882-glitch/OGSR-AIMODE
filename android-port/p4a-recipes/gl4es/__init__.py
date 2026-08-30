"""python-for-android recipe building gl4es for the target ABI.

The game draws with OpenGL 1.x - matrix stack, display lists, fixed
function lighting and fog, GL_QUADS, client-side vertex arrays. Android has
none of that: the device reports OpenGL ES 3.2, which is shader-only.
gl4es implements GL 1.5 on top of GLES2, so shipping it is far cheaper and
far more faithful than reimplementing the fixed-function pipeline.

Built with NOEGL and NOX11 because SDL has already created the context;
gl4es only needs to be told how to resolve GLES entry points, which
pyglet/gl.py does at initialize() time.
"""

import multiprocessing
import shutil
from os.path import exists, join

import sh
from pythonforandroid.logger import info, shprint
from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory


class GL4ESRecipe(Recipe):
    version = '1.1.6'
    url = 'https://github.com/ptitSeb/gl4es/archive/refs/tags/v{version}.tar.gz'
    name = 'gl4es'

    # Android extracts only libfoo.so from an APK, and the upstream target
    # is named libGL.so.1, so build_arch renames it before p4a looks.
    built_libraries = {'libgl4es.so': 'lib'}

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        build_dir = self.get_build_dir(arch.arch)
        toolchain = join(self.ctx.ndk_dir, 'build', 'cmake',
                         'android.toolchain.cmake')

        with current_directory(build_dir):
            shprint(
                sh.Command('cmake'), '.',
                '-DCMAKE_TOOLCHAIN_FILE={}'.format(toolchain),
                '-DANDROID_ABI={}'.format(arch.arch),
                '-DANDROID_PLATFORM=android-{}'.format(self.ctx.ndk_api),
                '-DANDROID=ON',
                '-DNOX11=ON',
                '-DNOEGL=ON',
                '-DUSE_ANDROID_LOG=ON',
                '-DCMAKE_BUILD_TYPE=Release',
                _env=env)
            shprint(sh.Command('make'), '-j', str(multiprocessing.cpu_count()),
                    'GL', _env=env)

            source = join(build_dir, 'lib', 'libGL.so.1')
            if not exists(source):
                raise RuntimeError('gl4es: %s was not produced' % source)
            target = join(build_dir, 'lib', 'libgl4es.so')
            shutil.copy(source, target)
            info('gl4es: installed as %s' % target)


recipe = GL4ESRecipe()
