from typing import List
from entities.ProteinEntity import ProteinEntity
from entities.OrganismEntity import OrganismEntity
from repositories.ProteinRepo import ProteinRepo

class ProteinUsecase:
    def __init__(self, protein_repo):
        self.protein_repo = protein_repo

    def get_protein(self, protein_id) -> ProteinEntity:
        protein = self.protein_repo.get(protein_id)
        return protein

    def get_infected(self) -> List[ProteinEntity]:
        proteins = self.protein_repo.get_all(True)
        return proteins

    def get_uninfected(self) -> List[ProteinEntity]:
        proteins = self.protein_repo.get_all(False)
        return proteins

    def create_protein(self, seq, infected, sex, org_mn, desc):
        organism = OrganismEntity(infected=infected, sex=sex, org_mnem=org_mn, desc=desc)
        protein = ProteinEntity(sequence=seq, organism=organism)
        protein = self.protein_repo.create(protein)
        return protein
