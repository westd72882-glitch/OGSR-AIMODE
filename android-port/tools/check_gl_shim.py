"""Import the shim off-device and check the names the game and the
controls actually reach for.

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

        bad = unresolved_input_symbols()
        if bad:
            print('android_input refers to undefined symbols: %s'
                  % ', '.join(bad))
            return 1

        failures = exercise_controls()
        if failures:
            for failure in failures:
                print('controls: %s' % failure)
            return 1

        print('shim imports; %d names defined, %d entry points stubbed out'
              % (len(used_names()), len(gl.MISSING)))
        print('touch controls resolve every symbol and behave correctly '
              '(stick, deadzone, drag vs tap, buttons)')
        return 0


def exercise_controls():
    """Drive the touch logic the way a thumb would and check what comes out.

    The controls have no toolkit under them, so the zones, the deadzone and
    the tap/hold split can all be tested here rather than by installing an
    APK and trying it.
    """
    from android_input import TouchControls
    from pyglet.window import key, mouse

    events = []
    controls = TouchControls(
        1000, 500,
        on_key=lambda symbol, pressed: events.append(('key', symbol, pressed)),
        on_button=lambda button, pressed: events.append(
            ('button', button, pressed)),
        on_look=lambda dx, dy: events.append(('look', dx, dy)))

    problems = []

    def expect(condition, message):
        if not condition:
            problems.append(message)

    # Left half: pushing the stick right and up should hold D and W, and
    # letting go should release both.
    controls.finger_down(1, 200.0, 250.0)
    controls.finger_move(1, 300.0, 340.0, 100.0, 90.0)
    expect(key.D in controls.held, 'pushing right did not hold D')
    expect(key.W in controls.held, 'pushing up did not hold W')
    expect(key.A not in controls.held, 'pushing right also held A')
    controls.finger_up(1, 300.0, 340.0)
    expect(not controls.held, 'releasing the stick left keys held: %s'
           % controls.held)

    # Inside the deadzone nothing should move.
    controls.finger_down(2, 200.0, 250.0)
    controls.finger_move(2, 202.0, 251.0, 2.0, 1.0)
    expect(not controls.held, 'a twitch inside the deadzone moved the player')
    controls.finger_up(2, 202.0, 251.0)

    # Right half: dragging looks, and a still tap breaks a block.
    events.clear()
    controls.finger_down(3, 800.0, 250.0)
    controls.finger_move(3, 830.0, 250.0, 30.0, 0.0)
    expect(any(event[0] == 'look' for event in events), 'dragging did not look')
    controls.finger_up(3, 830.0, 250.0)
    expect(not any(event[0] == 'button' for event in events),
           'a drag was mistaken for a tap')

    events.clear()
    controls.finger_down(4, 800.0, 250.0)
    controls.finger_up(4, 800.0, 250.0)
    expect(('button', mouse.LEFT, True) in events,
           'a still tap did not break a block')

    # The jump button must be reachable where it is drawn.
    events.clear()
    _name, symbol, bx, by, size = controls.button_rects()[0]
    expect(symbol == key.SPACE, 'the first button is not jump')
    controls.finger_down(5, bx + size / 2, by + size / 2)
    expect(key.SPACE in controls.held, 'pressing jump did not hold SPACE')
    controls.finger_up(5, bx + size / 2, by + size / 2)

    return problems


def unresolved_input_symbols():
    """Names android_input.py takes from the key and mouse tables.

    The controls are built out of pyglet symbols so they can be handed
    straight to the game later, which means a typo here is a crash on the
    device rather than anything Python notices at import.
    """
    import re

    from pyglet.window import key, mouse

    source = open(os.path.join(ROOT, 'android_input.py')).read()
    tables = {'key': key, 'mouse': mouse}
    bad = []
    for module, name in re.findall(r'\b(key|mouse)\.([A-Z_][A-Z_0-9]*)\b', source):
        if not hasattr(tables[module], name):
            bad.append('%s.%s' % (module, name))
    return sorted(set(bad))


if __name__ == '__main__':
    sys.exit(main())
