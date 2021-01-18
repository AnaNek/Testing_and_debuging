from repositories.ProteinRepo import ProteinRepo
from usecases.ProteinUsecase import ProteinUsecase

class ProteinFactory:
    @staticmethod
    def get_protein_usecase() -> ProteinUsecase:
        return ProteinUsecase(ProteinRepo())
