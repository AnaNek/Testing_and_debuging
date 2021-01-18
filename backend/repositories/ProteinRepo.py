from models_db.Protein import Protein
from models_db.Organism import Organism
from entities.ProteinEntity import ProteinEntity
from entities.OrganismEntity import OrganismEntity
from repositories.OrganismRepo import OrganismRepo
from typing import List

class ProteinRepo:
    @staticmethod
    def transform(protein) -> ProteinEntity:
        proteinEntity = ProteinEntity()
        organismEntity = OrganismEntity(infected=protein.organism.infected,
                                       org_mnem=protein.organism.organism_mnemonic,
                                       sex=protein.organism.sex, desc=protein.organism.description)

        proteinEntity.set(protein.id, protein.hash, protein.sequence, organismEntity)
        return proteinEntity

    @staticmethod
    def get(identify: int) -> ProteinEntity:
        protein = Protein.objects.get(id=identify)
        return ProteinRepo.transform(protein)

    @staticmethod
    def get_all(infected: bool) -> List[ProteinEntity]:
        try:
            organisms = Organism.objects.all().filter(infected=infected)
            set = [Protein.objects.all().filter(organism=organism) for organism in organisms]
            proteinsList = []
            for proteins in set:
                for protein in proteins:
                    proteinsList.append(ProteinRepo.transform(protein))
        except Protein.DoesNotExist as e:
            return []
        return proteinsList

    @staticmethod
    def create(proteinEntity):
        organism = Organism.objects.all().filter(infected=proteinEntity.organism.infected,
                                                organism_mnemonic=proteinEntity.organism.organism_mnemonic,
                                                sex=proteinEntity.organism.sex,
                                                description=proteinEntity.organism.description).first()
        if organism is None:
            organism = Organism(infected=proteinEntity.organism.infected,
                                organism_mnemonic=proteinEntity.organism.organism_mnemonic,
                                sex=proteinEntity.organism.sex,
                                description=proteinEntity.organism.description)
            organism.save()

        protein = Protein(sequence=proteinEntity.sequence, organism=organism)
        protein.save()
        return ProteinRepo.transform(protein)
