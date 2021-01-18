from models_db.Profile import Profile
from entities.ProfileEntity import ProfileEntity

class ProfileRepo:
    @staticmethod
    def transform(profile) -> ProfileEntity:
        profileEntity = ProfileEntity()
        profileEntity.set(profile.username, profile.password)
        return profileEntity

    @staticmethod
    def get(username) -> ProfileEntity:
        try:
            user = Profile.objects.get(username=username)
            return ProfileRepo.transform(user)
        except Profile.DoesNotExist:
            return None

    @staticmethod
    def create(profile):
        try:
            user = Profile(username=profile.username,
                           password=profile.password)
            user.save()
            return profile
        except IntegrityError as e:
            return None

    @staticmethod
    def update(profile):
        user = Profile.objects.get(username=profile.username)
        if not user:
            return None
        user.password = profile.password
        user.save()
        return profile
