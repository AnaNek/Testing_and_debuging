from models_db.Organism import Organism
from entities.OrganismEntity import OrganismEntity
from typing import List

class OrganismRepo:
    @staticmethod
    def transform(organism) -> OrganismEntity:
        organismEntity = OrganismEntity()
        organismEntity.set(organism.id,
        organism.infected, 
        organism.organism_mnemonic,
        organism.sex,
        organism.description)
        
        return organismEntity
        
    @staticmethod
    def get(organism_id) -> OrganismEntity:
        organism = Organism.objects.get(id=organism_id)
        return OrganismRepo.transform(organism)
        
    @staticmethod
    def get_all() -> List[OrganismEntity]:
        organisms = Organism.objects.objects.all()
        
        organism_entities = []
        
        for organism in organisms:
            organism_entities.append(OrganismRepo.transform(organism))
            
        return organism_entities

    @staticmethod
    def create(organism):
        try:
            organism = Organism(infected=organism.infected, 
            organism_mnemonic=organism.organism_mnemonic,
            sex=organism.sex,
            description=organism.description)
            organism.save()
        except IntegrityError as e:
            pass
