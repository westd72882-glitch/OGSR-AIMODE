

# ---------------------------------------------------------------------------
# gl4es start-up, and the bits of pyglet's API the game reaches for that are
# not GL entry points at all.
# ---------------------------------------------------------------------------

_FB_SIZE_CB = CFUNCTYPE(None, POINTER(c_int), POINTER(c_int))

#: Reported to gl4es as the size of the default framebuffer. initialize()
#: overwrites it with the real window size.
framebuffer_size = [1280, 720]


def _get_main_fb_size(width, height):
    width[0], height[0] = framebuffer_size


_fb_size_callback = _FB_SIZE_CB(_get_main_fb_size)  # kept alive deliberately


def initialize(size=None):
    """Start gl4es. The GL context must already be current.

    Built with NOEGL, gl4es does not create or look up a context itself -
    SDL has already made one - but it still needs a way to resolve GLES
    entry points and to learn the default framebuffer size, so both are
    handed to it here.
    """
    global INITIALIZED
    if INITIALIZED:
        return True
    if size:
        framebuffer_size[:] = [int(size[0]), int(size[1])]

    egl = ctypes.CDLL('libEGL.so')
    _lib.set_getprocaddress.argtypes = [c_void_p]
    _lib.set_getprocaddress(ctypes.cast(egl.eglGetProcAddress, c_void_p))
    _lib.set_getmainfbsize.argtypes = [_FB_SIZE_CB]
    _lib.set_getmainfbsize(_fb_size_callback)

    # Absent when gl4es was built with its init constructor left on, in
    # which case it initialised itself at dlopen and there is nothing to
    # call. The recipe disables that, but a binary built either way should
    # not take the app down here.
    try:
        _lib.initialize_gl4es()
    except AttributeError:
        MISSING.append('initialize_gl4es')

    INITIALIZED = True
    return True


def _string(name):
    value = ctypes.cast(glGetString(name), ctypes.c_char_p).value
    return value.decode('utf-8', 'replace') if value else ''


class GLInfo:
    """pyglet.gl.gl_info, narrowed to what the game asks it.

    Two answers here are deliberate rather than discovered. Occlusion
    queries are reported absent: gl4es does not implement the ARB entry
    points, and the game's only use of them is an optimisation it skips
    cleanly when the extension is missing. Versions above 1.5 are reported
    absent for the same reason - the one 3.2 branch in Minecraft.py asks
    for a core-profile mask that means nothing here.
    """

    #: Anything above this makes the game take a path gl4es cannot serve.
    MAX_VERSION = (1, 5)

    def get_version(self):
        return _string(GL_VERSION) or '1.5 gl4es'

    def get_renderer(self):
        return _string(GL_RENDERER)

    def get_vendor(self):
        return _string(GL_VENDOR)

    def get_extensions(self):
        return _string(GL_EXTENSIONS).split()

    def have_extension(self, name):
        if 'occlusion_query' in name:
            return False
        return name in self.get_extensions()

    def have_version(self, major, minor=0):
        return (major, minor) <= self.MAX_VERSION


gl_info = GLInfo()
