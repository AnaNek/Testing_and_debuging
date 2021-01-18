class PatternEntity(object):
    def __init__(self, id=None, hash=None, subsequence=None, start_pos=None, end_pos=None):
        self._id = id
        self._hash = hash
        self._subsequence = subsequence
        self._start_pos = start_pos
        self._end_pos = end_pos

    def set(
        self,
        id: int,
        hash: str,
        subsequence: str,
        start_pos: int,
        end_pos: int
    ):
        self._id = id
        self._hash = hash
        self._subsequence = subsequence
        self._start_pos = start_pos
        self._end_pos = end_pos

        return self

    def set_hash(
        self,
        hash: str
    ):
        self._hash = hash

        return self

    @property
    def id(self):
        return self._id

    @property
    def hash(self):
        return self._hash

    @property
    def subsequence(self):
        return self._subsequence

    @property
    def start_pos(self):
        return self._start_pos

    @property
    def end_pos(self):
        return self._end_pos
