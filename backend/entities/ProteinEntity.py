from entities.OrganismEntity import OrganismEntity

class ProteinEntity(object):
    def __init__(self, id=None, hash=None, sequence=None, organism=None):
        self._id = id
        self._hash = hash
        self._sequence = sequence
        self._organism = organism

    def set(
        self,
        id: int,
        hash: str,
        sequence: str,
        organism: OrganismEntity,
    ):
        self._id = id
        self._hash = hash
        self._sequence = sequence
        self._organism = organism

        return self

    @property
    def id(self):
        return self._id

    @property
    def hash(self):
        return self._hash

    @property
    def sequence(self):
        return self._sequence

    @property
    def organism(self):
        return self._organism
