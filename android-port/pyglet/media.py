"""pyglet.media, silent.

Sound is the one part of the port with no path through gl4es or SDL yet:
the game's sounds are .ogg files it loads by URL. Rather than let that
crash a world that otherwise runs, every player here accepts the calls the
sound manager makes - position, pitch, volume, pause, delete - and plays
nothing. Replacing this with SDL_mixer, which the APK already contains, is
a self-contained job.
"""


class Listener:
    position = (0.0, 0.0, 0.0)
    forward_orientation = (0.0, 0.0, -1.0)
    up_orientation = (0.0, 1.0, 0.0)
    volume = 1.0


class Player:
    def __init__(self):
        self.position = (0.0, 0.0, 0.0)
        self.volume = 1.0
        self.pitch = 1.0
        self.priority = 0
        self.min_distance = 0.0
        self.max_distance = 0.0
        self.playing = False

    def queue(self, source):
        pass

    def play(self):
        self.playing = True
        return self

    def pause(self):
        self.playing = False

    def delete(self):
        self.playing = False

    def seek(self, timestamp):
        pass


class _Source:
    def play(self):
        return Player()


class _AudioDriver:
    def __init__(self):
        self._listener = Listener()

    def get_listener(self):
        return self._listener


_driver = _AudioDriver()


def get_audio_driver():
    return _driver


def load(name, streaming=True):
    return _Source()


def have_ffmpeg():
    return False
