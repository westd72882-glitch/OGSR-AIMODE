"""Import the generated GL shim off-device, against a stub library.

pyglet/gl.py is 340 lines of generated declarations that nothing on this
machine can exercise: there is no gl4es here, and no GL context. But the
failure that cost a build - a type alias emitted before the alias it was
defined from - was a plain NameError at import, and a stub library with no
symbols at all is enough to provoke it. Every entry point simply lands in
MISSING, which is exactly what the module is designed to tolerate.

    python tools/check_gl_shim.py
"""

import importlib
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def build_stub(directory):
    source = os.path.join(directory, 'stub.c')
    library = os.path.join(directory, 'libgl4es_stub.so')
    with open(source, 'w') as handle:
        handle.write('void gl4es_stub(void) {}\n')
    subprocess.run(['gcc', '-shared', '-fPIC', '-o', library, source], check=True)
    return library


def used_names():
    out = subprocess.run(
        ['grep', '-rhoE', r'\bgl\.[A-Za-z_0-9]+', os.path.join(ROOT, 'game', 'mc')],
        capture_output=True, text=True, check=True).stdout
    return sorted({line[3:] for line in out.split('\n') if line.startswith('gl.')})


def main():
    with tempfile.TemporaryDirectory() as directory:
        os.environ['GL4ES_LIBRARY'] = build_stub(directory)
        sys.path.insert(0, ROOT)
        gl = importlib.import_module('pyglet.gl')

        missing = [name for name in used_names() if not hasattr(gl, name)]
        if missing:
            print('NOT DEFINED: %s' % ', '.join(missing))
            return 1

        for method in ('get_version', 'get_renderer', 'get_vendor',
                       'have_extension', 'have_version'):
            if not callable(getattr(gl.gl_info, method, None)):
                print('gl_info.%s is missing' % method)
                return 1
        if gl.gl_info.have_version(3, 0) or gl.gl_info.have_extension(
                'GL_ARB_occlusion_query'):
            print('gl_info advertises a capability gl4es cannot serve')
            return 1

        print('shim imports; %d names defined, %d entry points stubbed out'
              % (len(used_names()), len(gl.MISSING)))
        return 0


if __name__ == '__main__':
    sys.exit(main())
