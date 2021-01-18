from repositories.OrganismRepo import OrganismRepo
from usecases.OrganismUsecase import OrganismUsecase

class OrganismFactory:
    @staticmethod
    def get_organism_usecase() -> OrganismUsecase:
        return OrganismUsecase(OrganismRepo())
