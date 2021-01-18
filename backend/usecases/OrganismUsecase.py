from typing import List
from entities.OrganismEntity import OrganismEntity
from repositories.OrganismRepo import OrganismRepo

class OrganismUsecase:
    def __init__(self, organism_repo):
        self.organism_repo = organism_repo

    def get_organism(self, organism_id) -> OrganismEntity:
        organism = self.organism_repo.get(organism_id)
        return protein

    def get_all_organisms(self) -> List[OrganismEntity]:
        organisms = self.organism_repo.get_all()
        return organisms
                
    def create_organism(self, organism):
        self.organism_repo.create(organism)
