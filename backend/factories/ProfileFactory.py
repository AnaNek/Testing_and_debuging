from repositories.ProfileRepo import ProfileRepo
from usecases.ProfileUsecase import ProfileUsecase

class ProfileFactory:
    @staticmethod
    def get_profile_usecase() -> ProfileUsecase:
        return ProfileUsecase(ProfileRepo())
