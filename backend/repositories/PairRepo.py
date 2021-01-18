from models_db.Protein import Protein
from models_db.ProteinPair import ProteinPair
from entities.ProteinPairEntity import ProteinPairEntity
from entities.ProteinEntity import ProteinEntity
from entities.ProteinPairEntity import ProteinPairEntity
from repositories.ProteinRepo import ProteinRepo
from typing import List

class PairRepo:
    @staticmethod
    def transform(pair, protein1, protein2):
        pairEntity = ProteinPairEntity()
        
        pairEntity.set(pair.id, ProteinRepo.transform(protein1), ProteinRepo.transform(protein2),
                       pair.similarity, pair.pattern_count)
        return pairEntity
        
    @staticmethod
    def get_by_ids(id1, id2) -> ProteinPairEntity:
        try:
            protein1 = Protein.objects.get(id=id1)
            protein2 = Protein.objects.get(id=id2)
            pair = ProteinPair.objects.all().filter(protein1=protein1, protein2=protein2).first()
            if pair is None:
                pair = ProteinPair.objects.all().filter(protein1=protein2, protein2=protein1).first()
                if pair is None:
                    return None
            return PairRepo.transform(pair, protein1, protein2)
            
        except Protein.DoesNotExist as e:
            return None
