from entities.ProteinPairEntity import ProteinPairEntity
from entities.PatternEntity import PatternEntity
from typing import List

class ResultEntity(object):
    def __init__(self, pair=None, patterns=None):
        self._pair = pair
        self._patterns = patterns

    def set(
        self,
        pair: ProteinPairEntity,
        patterns: List[PatternEntity]
    ):
        self._id = id
        self._pair = pair
        self._patterns = patterns

        return self

    @property
    def pair(self):
        return self._pair

    @property
    def patterns(self):
        return self._patterns
