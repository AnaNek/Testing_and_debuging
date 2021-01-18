class OrganismEntity(object):
    def __init__(self, id=None, infected=None, org_mnem=None, sex=None, desc=None):
        self._id = id
        self._infected = infected
        self._organism_mnemonic = org_mnem
        self._sex = sex
        self._description = desc

    def set(
        self,
        organism_id: int,
        infected: bool,
        organism_mnemonic: str,
        sex: str,
        description: str
    ):
        self._id = organism_id
        self._organism_mnemonic = organism_mnemonic
        self._infected = infected
        self._sex = sex
        self._description = description

        return self

    @property
    def id(self):
        return self._id

    @property
    def organism_mnemonic(self):
        return self._organism_mnemonic

    @property
    def infected(self):
        return self._infected

    @property
    def sex(self):
        return self._sex

    @property
    def description(self):
        return self._description
