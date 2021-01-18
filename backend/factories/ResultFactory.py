from repositories.ResultRepo import ResultRepo
from usecases.ResultUsecase import ResultUsecase

class ResultFactory:
    @staticmethod
    def get_result_usecase() -> ResultUsecase:
        return ResultUsecase(ResultRepo())
