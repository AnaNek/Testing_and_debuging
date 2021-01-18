from models_db.ResultSet import ResultSet
from models_db.Protein import Protein
from models_db.ProteinPair import ProteinPair
from models_db.Profile import Profile
from models_db.Pattern import Pattern
from entities.PatternEntity import PatternEntity
from entities.ResultEntity import ResultEntity
from entities.ProteinPairEntity import ProteinPairEntity
from repositories.PairRepo import PairRepo
from typing import List

import logging
logger = logging.getLogger(__name__)

class ResultRepo:
    @staticmethod
    def transform(pair, protein1, protein2, set):
        resultEntity = ResultEntity()
        n = len(set)
        patterns = []
        for i in range(n):
            patternEntity = PatternEntity()
            patternEntity.set(set[i].pattern.id, set[i].pattern.hash, set[i].pattern.subsequence,
                              set[i].pattern.start_pos, set[i].pattern.end_pos)
            patterns.append(patternEntity)

        resultEntity.set(PairRepo.transform(pair, protein1, protein2), patterns)
        return resultEntity

    @staticmethod
    def get_by_pair(pair_id: int) -> ResultEntity:
        try:
            pair = ProteinPair.objects.get(id=pair_id)
            protein1 = pair.protein1
            protein2 = pair.protein2
            pair = ProteinPair.objects.all().filter(protein1=protein1, protein2=protein2).first()
            if pair is not None:
                set = ResultSet.objects.all().filter(protein_pair=pair)
                result = ResultRepo.transform(pair, protein1, protein2, set)
                return result
            pair = ProteinPair.objects.all().filter(protein1=protein2, protein2=protein1).first()
            if pair is not None:
                set = ResultSet.objects.all().filter(protein_pair=pair)
                result = ResultRepo.transform(pair, protein1, protein2, set)
                return result
            return None

        #except (Protein.DoesNotExist) as e:
        #    raise NotFound()
        except (ProteinPair.DoesNotExist) as e:
            return None
        return None

    @staticmethod
    def get_by_proteins(protein_id1: int, protein_id2: int) -> ResultEntity:
        try:
            protein1 = Protein.objects.get(id=protein_id1)
            protein2 = Protein.objects.get(id=protein_id2)
            pair = ProteinPair.objects.all().filter(protein1=protein1, protein2=protein2).first()
            if pair is not None:
                set = ResultSet.objects.all().filter(protein_pair=pair)
                result = ResultRepo.transform(pair, protein1, protein2, set)
                return result
            pair = ProteinPair.objects.all().filter(protein1=protein2, protein2=protein1).first()
            if pair is not None:
                set = ResultSet.objects.all().filter(protein_pair=pair)
                result = ResultRepo.transform(pair, protein1, protein2, set)
                return result
            return None

        except (ProteinPair.DoesNotExist) as e:
            return None
        return None

    @staticmethod
    def create(pair, patterns, username=None):
        try:
            #user = Profile.objects.get(username=username)
            protein1 = Protein.objects.get(id=pair.protein1.id)
            protein2 = Protein.objects.get(id=pair.protein2.id)
            _pair = ProteinPair.objects.all().filter(protein1=protein1, protein2=protein2).first()
            if _pair is None:
                _pair = ProteinPair.objects.all().filter(protein1=protein2, protein2=protein1).first()
                if _pair is None:
                    _pair = ProteinPair(protein1=protein1, protein2=protein2, pattern_count=pair.pattern_count, 
                                        similarity=pair.similarity)
                    _pair.save()

            n = len(patterns)
            for i in range(n):
                pattern = Pattern.objects.all().filter(subsequence=patterns[i].subsequence,
                                                   start_pos=patterns[i].start_pos,
                                                   end_pos=patterns[i].end_pos).first()
                if pattern is None:
                    pattern = Pattern(subsequence=patterns[i].subsequence,
                                      start_pos=patterns[i].start_pos,
                                      end_pos=patterns[i].end_pos)
                    pattern.save()

                res = ResultSet(protein_pair=_pair, pattern=pattern)
                res.save()

                #user_result = UserResult(user=user, result_set=res)
                #user_result.save()

        except (Profile.DoesNotExist, Protein.DoesNotExist) as e:
            pass
