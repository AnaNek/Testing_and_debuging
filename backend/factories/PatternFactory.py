from repositories.PatternRepo import PatternRepo
from usecases.PatternUsecase import PatternUsecase

class PatternFactory:
    @staticmethod
    def get_pattern_usecase() -> PatternUsecase:
        return PatternUsecase(PatternRepo())
