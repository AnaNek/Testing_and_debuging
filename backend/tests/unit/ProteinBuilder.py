from models_db.Protein import Protein
from tests.unit.OrganismBuilder import OrganismBuilder

class ProteinBuilder:
    def __init__(self):
        self.sequence = ""
        self.organism = OrganismBuilder().build()
        self.protein = Protein.objects.create(sequence=self.sequence,
                               organism=self.organism)
        
    def with_sequence(self, seq):
        self.protein.sequence = seq
        self.protein.save()
        return self
        
    def with_organism(self, org):
        self.protein.organism = org
        self.protein.save()
        return self
        
    def build(self):
        return self.protein
