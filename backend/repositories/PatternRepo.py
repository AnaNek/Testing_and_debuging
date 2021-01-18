from models_db.Pattern import Pattern
from entities.PatternEntity import PatternEntity
from typing import List

class PatternRepo:
    @staticmethod
    def transform(pattern) -> PatternEntity:
        patternEntity = PatternEntity()
        patternEntity.set(pattern.id, pattern.hash, pattern.subsequence,
                          pattern.start_pos, pattern.end_pos)
        return patternEntity
        
    @staticmethod
    def get(identify: int) -> PatternEntity:
        pattern = Pattern.objects.get(id=identify)
        return PatternRepo.transform(pattern)

    @staticmethod
    def get_hash(patternEntity) -> str:
        empty_str = ''
        try:
            pattern = Pattern.objects.all().filter(subsequence=patternEntity.subsequence,
                                                   start_pos=patternEntity.start_pos,
                                                   end_pos=patternEntity.end_pos).first()
            if pattern is not None:
                return pattern.hash
            return empty_str
        except Pattern.DoesNotExist as e:
            return empty_str

    @staticmethod
    def create(patternEntity):
        try:
            pattern = Pattern(subsequence=patternEntity.subsequence,
                              start_pos=patternEntity.start_pos,
                              end_pos=patternEntity.end_pos)
            pattern.save()
        except IntegrityError as e:
            pass
