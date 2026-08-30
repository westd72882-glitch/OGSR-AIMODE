"""Android entry point: start the game, and never fail silently.

Everything before this file was scaffolding to make the game runnable -
the Cython modules cross-compiled, OpenGL 1.x provided by gl4es, the
pyglet API the game expects. This starts it.

A black screen taught the expensive lesson here: on Android a crash before
the first frame is invisible. So the readiness report still runs, but into
a file rather than a window, and any failure to launch is written there in
full before the process is allowed to end.
"""

import os
import sys
import traceback

LOG_NAME = 'port-check.txt'
PACKAGE = 'org.mcpython.mcpython'


def log_path():
    """A file a file manager can reach, so a crash is recoverable.

    An app's own directory under /sdcard/Android/data needs no permission
    and stays browsable. The private directory is the fallback; it keeps
    the code path identical even when it cannot be read off the device.
    """
    try:
        from android.storage import primary_external_storage_path
        base = os.path.join(primary_external_storage_path(),
                            'Android', 'data', PACKAGE, 'files')
        os.makedirs(base, exist_ok=True)
    except Exception:
        base = os.environ.get('ANDROID_PRIVATE') or os.getcwd()
    return os.path.join(base, LOG_NAME)


_lines = []


def record(text):
    """Append to the report and flush it, so a hard crash keeps the tail."""
    _lines.append(text)
    print(text)  # p4a routes stdout to logcat
    try:
        with open(log_path(), 'w') as handle:
            handle.write('\n'.join(_lines) + '\n')
    except Exception:
        pass


def prepare_environment():
    """Give the game a writable home.

    It creates ~/.minecraft for its options and saves, and HOME on Android
    is not somewhere an app may write.
    """
    private = os.environ.get('ANDROID_PRIVATE') or os.getcwd()
    os.environ['HOME'] = private
    sys.argv = ['minecraft']
    return private


def probe(label, function):
    try:
        record('%s: %s' % (label, function()))
    except BaseException:
        detail = traceback.format_exc().strip().splitlines()
        record('%s: FAIL\n    %s' % (label, '\n    '.join(detail[-4:])))


def report_readiness():
    """The import-level checks, without a window.

    Anything needing a GL context is left to the game: it creates the
    context, and a probe that made one first would be competing with it.
    """
    record('python: %d.%d.%d' % sys.version_info[:3])
    probe('numpy', lambda: __import__('numpy').__version__)
    probe('pillow', lambda: __import__('PIL').__version__)
    probe('nbtlib', lambda: __import__('nbtlib').__version__)

    def gl_binding():
        from pyglet import gl
        return '%d entry points missing%s' % (
            len(gl.MISSING),
            (': ' + ', '.join(gl.MISSING[:6])) if gl.MISSING else '')

    probe('pyglet gl', gl_binding)

    def textures():
        from mc import Resources
        return '%d textures' % len(Resources.textures)

    probe('game resources', textures)


def launch():
    from mc.net.minecraft.client.Minecraft import Minecraft
    from mc.net.minecraft.client.Session import Session

    record('starting the game')
    # Fullscreen from the start: a phone has no other mode, and it keeps
    # the game off the desktop-centring path it would otherwise take.
    game = Minecraft(True, False, width=854, height=480, resizable=True,
                     vsync=False, visible=False, caption='Minecraft Indev')
    game.session = Session('player', '')
    game.run()


def distress():
    """Hold a red screen so a launch failure is visible, not just logged.

    Only possible when a window survived long enough to exist; without one
    the report file is the whole story, which is why it is written first.
    """
    try:
        import time

        from pyglet import gl
        from pyglet.window import _windows

        if not _windows:
            return
        window = _windows[0]
        deadline = time.monotonic() + 20.0
        while time.monotonic() < deadline:
            gl.glClearColor(0.45, 0.05, 0.05, 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            window.dispatch_events()
            window.flip()
            time.sleep(0.05)
    except Exception:
        pass


def main():
    home = prepare_environment()
    record('port readiness')
    record('log: %s' % log_path())
    record('home: %s' % home)
    record('')
    report_readiness()
    record('')

    try:
        launch()
    except BaseException:
        record('LAUNCH FAILED\n%s' % traceback.format_exc())
        distress()
        raise


if __name__ == '__main__':
    main()
