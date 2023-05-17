
class FrameCouples:
    _frames = []
    _current = -1

    def __init__(cls,l=10):
        print(f"Creating new Frames with length {l}")
        for i in range(l):
            cls._frames.append(None)

    def getAll(self):
        return self._frames

    def update(self,data):
        self._current = self._current + 1
        if self._current >= len(self._frames):
            self._current = 0
        self._frames[self._current] = data

