from typing import List
from entities.PatternEntity import PatternEntity
from repositories.PatternRepo import PatternRepo

class PatternUsecase:
    def __init__(self, pattern_repo):
        self.pattern_repo = pattern_repo

    def get_pattern(self, pattern_id) -> PatternEntity:
        pattern = self.pattern_repo.get(pattern_id)
        return pattern
        
    def get_pattern_hash(self, patternEntity) -> str:
        pattern_hash = self.pattern_repo.get_hash(atternEntity)
        return pattern_hash
                
    def create_pattern(self, pattern):
        self.pattern_repo.create(pattern)
