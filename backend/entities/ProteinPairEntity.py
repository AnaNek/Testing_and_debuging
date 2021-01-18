from typing import List
from entities.ProteinEntity import ProteinEntity
from entities.PatternEntity import PatternEntity

import logging
logger = logging.getLogger(__name__)

class ProteinPairEntity(object):
    def __init__(self, id=None, protein1=None, protein2=None,
                       similarity=0, pattern_count=None):
        self._id = id
        self._protein1 = protein1
        self._protein2 = protein2
        self._similarity = similarity
        self._pattern_count = pattern_count

    def set(
        self,
        id: int,
        protein1: ProteinEntity,
        protein2: ProteinEntity,
        similarity,
        pattern_count
    ):
        self._id = id
        self._protein1 = protein1
        self._protein2 = protein2
        self._similarity = similarity
        self._pattern_count = pattern_count

        return self

    def set_proteins(
        self,
        protein1: ProteinEntity,
        protein2: ProteinEntity,
    ):
        self._protein1 = protein1
        self._protein2 = protein2

        return self

    def set_similarity(
        self,
        similarity
    ):
        self._similarity = similarity

        return self

    def set_count(
        self,
        count
    ):
        self._pattern_count = count

        return self

    @property
    def id(self):
        return self._id

    @property
    def protein1(self):
        return self._protein1

    @property
    def protein2(self):
        return self._protein2

    @property
    def similarity(self):
        return self._similarity

    @property
    def pattern_count(self):
        return self._pattern_count

    def compare(self):
        seq1 = self._protein1.sequence
        seq2 = self._protein2.sequence
        l = len(seq1)
        m = len(seq2)
        if l != m:
            l = min(l, m)
            m = max(l, m)
        prev = -1
        patterns = []
        pattern = []
        count = 0
        for i in range(l):
            if seq1[i] != seq2[i]:
                if (i - prev) > 1:
                    pattern = PatternEntity()
                    pattern.set(None, None, seq1[prev+1:i], prev+1, i-1)
                    patterns.append(pattern)
                prev = i
                count += 1
            elif i == l-1:
                pattern = PatternEntity()
                pattern.set(None, None, seq1[prev+1:i+1], prev+1, i)
                patterns.append(pattern)

        if m:
            similarity = 100 * (l - count) / m
        else:
            similarity = 100

        self._similarity = similarity
        self._pattern_count = len(patterns)

        return patterns
