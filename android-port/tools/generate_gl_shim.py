"""Generate android-port/pyglet/gl.py from a real pyglet installation.

The game calls 141 distinct names on pyglet's gl module. Retyping their
ctypes signatures by hand would be 141 chances to get an enum value or an
argument type silently wrong, so read them out of pyglet's own generated
bindings instead and emit ctypes declarations bound to gl4es.

    pip install pyglet==1.5.31 && python tools/generate_gl_shim.py
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'pyglet', 'gl.py')

ALIAS = re.compile(r'^(GL\w+) = ((?:c_\w+|None|POINTER\([^\n]*?\)|CFUNCTYPE\([^\n]*?\)))\s*(?:#.*)?$')
CONST = re.compile(r'^(GL_\w+) = (-?\d+|\d+\.\d+)\s*(?:#.*)?$')
FUNC = re.compile(r"^(gl\w+) = _link_function\('(\w+)', (.+?), \[(.*?)\], .*\)\s*$")


def pyglet_sources():
    import pyglet
    base = os.path.join(os.path.dirname(pyglet.__file__), 'gl')
    return [os.path.join(base, name) for name in ('gl.py', 'glext_arb.py')]


def harvest():
    # Aliases keep pyglet's own file order: several are defined in terms of
    # earlier ones (GLhandleARB = GLuint), so sorting them alphabetically
    # emits a forward reference that only fails at import time on the device.
    aliases, consts, funcs = {}, {}, {}
    for path in pyglet_sources():
        with open(path) as handle:
            for line in handle:
                line = line.rstrip('\n')
                m = ALIAS.match(line)
                if m and m.group(1) not in aliases:
                    aliases[m.group(1)] = m.group(2)
                    continue
                m = CONST.match(line)
                if m and m.group(1) not in consts:
                    consts[m.group(1)] = m.group(2)
                    continue
                m = FUNC.match(line)
                if m and m.group(1) not in funcs:
                    funcs[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    return aliases, consts, funcs


#: Not referenced by the game, but the epilogue's gl_info needs them and a
#: caller debugging a blank frame will want glGetError.
FORCE = ('GL_VERSION', 'GL_RENDERER', 'GL_VENDOR', 'GL_EXTENSIONS',
         'glGetString', 'glGetError')


def wanted():
    """Every gl.<name> the game source refers to, plus FORCE."""
    out = subprocess.run(
        ['grep', '-rhoE', r'\bgl\.[A-Za-z_0-9]+', os.path.join(ROOT, 'game', 'mc')],
        capture_output=True, text=True, check=True).stdout
    found = {line[3:] for line in out.split('\n') if line.startswith('gl.')}
    return sorted(found | set(FORCE))


#: Names the prologue already brings into scope.
PRELUDE = frozenset((
    'CFUNCTYPE', 'POINTER', 'None', 'ctypes', 'c_ptrdiff_t',
    'c_char', 'c_double', 'c_float', 'c_int', 'c_int64', 'c_short',
    'c_ubyte', 'c_uint', 'c_uint64', 'c_ushort', 'c_void_p',
))

IDENT = re.compile(r'[A-Za-z_]\w*')


def resolvable(aliases):
    """Drop aliases that name something we do not emit.

    pyglet declares a few types over ctypes Structures it defines inline
    (GLsync = POINTER(struct___GLsync)). Copying only the alias leaves a
    forward reference that raises at import - on the device, after a
    fifteen minute build. None of them are names the game uses, so keeping
    an alias only when every name in it already resolves is both safe and
    the only rule that cannot produce this class of failure again.
    """
    known = set(PRELUDE)
    kept, dropped = {}, []
    for name, value in aliases.items():
        unresolved = [word for word in IDENT.findall(value) if word not in known]
        if unresolved:
            dropped.append('%s (needs %s)' % (name, ', '.join(sorted(set(unresolved)))))
            continue
        kept[name] = value
        known.add(name)
    return kept, dropped


def main():
    aliases, consts, funcs = harvest()
    names = wanted()

    used_consts, used_funcs, used_aliases, missing = [], [], [], []
    for name in names:
        if name in consts:
            used_consts.append(name)
        elif name in funcs:
            used_funcs.append(name)
        elif name in aliases:
            used_aliases.append(name)
        else:
            missing.append(name)

    aliases, dropped = resolvable(aliases)

    body = []
    body.append('# Type aliases, in pyglet\'s own order: some are defined in')
    body.append('# terms of earlier ones, so this order is load-bearing.')
    for name, value in aliases.items():
        body.append('%s = %s' % (name, value))

    body.append('')
    body.append('')
    body.append('# Enumerants.')
    for name in used_consts:
        body.append('%s = %s' % (name, consts[name]))

    body.append('')
    body.append('')
    body.append('# Entry points. _fn() records anything gl4es does not export')
    body.append('# in MISSING rather than failing the import, so a gap shows up')
    body.append('# as a diagnostic instead of a crash on a black screen.')
    for name in used_funcs:
        symbol, restype, argtypes = funcs[name]
        body.append("%s = _fn('%s', %s, [%s])" % (name, symbol, restype, argtypes))

    with open(os.path.join(HERE, 'gl_prologue.py')) as handle:
        prologue = handle.read()
    with open(os.path.join(HERE, 'gl_epilogue.py')) as handle:
        epilogue = handle.read()

    with open(OUT, 'w') as handle:
        handle.write(prologue)
        handle.write('\n'.join(body))
        handle.write('\n')
        handle.write(epilogue)

    print('wrote %s' % OUT)
    print('constants %d, functions %d, aliases %d' % (
        len(used_consts), len(used_funcs), len(used_aliases)))
    print('not found in pyglet: %s' % (', '.join(missing) or 'none'))
    print('aliases dropped as unresolvable: %s' % (', '.join(dropped) or 'none'))


if __name__ == '__main__':
    sys.exit(main())
