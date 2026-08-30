"""The slice of SDL2 the window shim needs, bound through ctypes.

p4a's sdl2 bootstrap already ships libSDL2 in the APK and hands control to
main.py with the Java surface in place; creating the window and the GL
context from Python is what Kivy would otherwise do here. Only the calls
the game's loop actually makes are bound - about fifteen of them - rather
than pulling in a whole SDL binding.
"""

import ctypes
from ctypes import (POINTER, Structure, c_char_p, c_float, c_int, c_int32,
                    c_int64, c_uint8, c_uint32, c_void_p)

#: Populated by load(). Deliberately not loaded at import: the game
#: imports pyglet.window for its key tables long before it makes a window,
#: and binding SDL that early would make those imports need a device.
lib = None

INIT_VIDEO = 0x00000020
INIT_EVENTS = 0x00004000

WINDOWPOS_UNDEFINED = 0x1FFF0000
WINDOW_FULLSCREEN = 0x00000001
WINDOW_OPENGL = 0x00000002
WINDOW_SHOWN = 0x00000004
WINDOW_RESIZABLE = 0x00000020

GL_RED_SIZE = 0
GL_GREEN_SIZE = 1
GL_BLUE_SIZE = 2
GL_ALPHA_SIZE = 3
GL_DOUBLEBUFFER = 5
GL_DEPTH_SIZE = 6
GL_STENCIL_SIZE = 7
GL_CONTEXT_MAJOR_VERSION = 17
GL_CONTEXT_MINOR_VERSION = 18
GL_CONTEXT_PROFILE_MASK = 21
GL_CONTEXT_PROFILE_ES = 0x0004

QUIT = 0x100
WINDOWEVENT = 0x200
KEYDOWN = 0x300
KEYUP = 0x301
TEXTINPUT = 0x303
FINGERDOWN = 0x700
FINGERUP = 0x701
FINGERMOTION = 0x702

WINDOWEVENT_RESIZED = 5
WINDOWEVENT_SIZE_CHANGED = 6
WINDOWEVENT_FOCUS_GAINED = 12
WINDOWEVENT_FOCUS_LOST = 13


class TouchFingerEvent(Structure):
    # Field order and types follow SDL_TouchFingerEvent exactly; ctypes'
    # natural alignment then reproduces SDL's layout, which is why touchId
    # lands at offset 8 as it must.
    _fields_ = [
        ('type', c_uint32), ('timestamp', c_uint32),
        ('touchId', c_int64), ('fingerId', c_int64),
        ('x', c_float), ('y', c_float),
        ('dx', c_float), ('dy', c_float),
        ('pressure', c_float), ('windowID', c_uint32),
    ]


class KeysymStruct(Structure):
    _fields_ = [('scancode', c_int32), ('sym', c_int32),
                ('mod', c_uint32), ('unused', c_uint32)]


class KeyboardEvent(Structure):
    _fields_ = [
        ('type', c_uint32), ('timestamp', c_uint32), ('windowID', c_uint32),
        ('state', c_uint8), ('repeat', c_uint8),
        ('padding2', c_uint8), ('padding3', c_uint8),
        ('keysym', KeysymStruct),
    ]


class WindowEvent(Structure):
    _fields_ = [
        ('type', c_uint32), ('timestamp', c_uint32), ('windowID', c_uint32),
        ('event', c_uint8),
        ('padding1', c_uint8), ('padding2', c_uint8), ('padding3', c_uint8),
        ('data1', c_int32), ('data2', c_int32),
    ]


#: SDL_Event is a union padded to 56 bytes; 64 is safely larger and the
#: individual events are read by casting this buffer.
EVENT_SIZE = 64


#: name -> (restype, argtypes), bound onto this module by load().
_SIGNATURES = {
    'Init': ('SDL_Init', c_int, [c_uint32]),
    'InitSubSystem': ('SDL_InitSubSystem', c_int, [c_uint32]),
    'GetError': ('SDL_GetError', c_char_p, []),
    'GL_SetAttribute': ('SDL_GL_SetAttribute', c_int, [c_int, c_int]),
    'CreateWindow': ('SDL_CreateWindow', c_void_p,
                     [c_char_p, c_int, c_int, c_int, c_int, c_uint32]),
    'GL_CreateContext': ('SDL_GL_CreateContext', c_void_p, [c_void_p]),
    'GL_MakeCurrent': ('SDL_GL_MakeCurrent', c_int, [c_void_p, c_void_p]),
    'GL_SwapWindow': ('SDL_GL_SwapWindow', None, [c_void_p]),
    'GL_SetSwapInterval': ('SDL_GL_SetSwapInterval', c_int, [c_int]),
    'GetWindowSize': ('SDL_GetWindowSize', None,
                      [c_void_p, POINTER(c_int), POINTER(c_int)]),
    'PollEvent': ('SDL_PollEvent', c_int, [c_void_p]),
    'DestroyWindow': ('SDL_DestroyWindow', None, [c_void_p]),
}


def load():
    """Bind libSDL2. Safe to call repeatedly; the first call does the work."""
    global lib
    if lib is not None:
        return lib

    lib = ctypes.CDLL('libSDL2.so')
    for attribute, (symbol, restype, argtypes) in _SIGNATURES.items():
        func = getattr(lib, symbol)
        func.restype = restype
        func.argtypes = argtypes
        globals()[attribute] = func
    return lib


def error():
    message = GetError()
    return message.decode('utf-8', 'replace') if message else 'unknown error'
