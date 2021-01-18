from django.test import TestCase
from repositories.ProfileRepo import ProfileRepo
from entities.ProfileEntity import ProfileEntity
from models_db.Profile import Profile

class TestProfileRepo(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "somename"
        cls.profile = Profile.objects.create(username=cls.username)

    def test_get_profile(self):
        # Arrange
        username = self.username
        profile = self.profile
        profile_repo = ProfileRepo()

        # Act
        profileEntity = profile_repo.get(username)

        # Assert
        self.assertEqual(profile.username, profileEntity.username)

    def test_get_profile_not_exist(self):
        # Arrange
        username = "bad_username"
        profile_repo = ProfileRepo()

        # Act
        profileEntity = profile_repo.get(username)

        # Assert
        self.assertIsNone(profileEntity)

    def test_create_profile(self):
        # Arrange
        username = "newuser"
        password = "newpassword"
        profile = ProfileEntity(username, password)
        profile_repo = ProfileRepo()

        #Act
        profile_repo.create(profile)
        created_profile = Profile.objects.all().filter(username=username, password=password).first()
        created_profile = {'_username': created_profile.username, '_password': created_profile.password}

        # Assert
        self.assertDictEqual(profile.__dict__, created_profile)

    def test_update_profile(self):
        # Arrange
        username = self.username
        profile = self.profile
        password = "somepassword"
        expected_profile = ProfileEntity(username, password).__dict__
        profileEntity = ProfileEntity(username, password)
        profile_repo = ProfileRepo()

        # Act
        updated_profile = profile_repo.update(profileEntity)
        updated_profile = updated_profile.__dict__
        profile.refresh_from_db()

        # Assert
        self.assertEqual(updated_profile, expected_profile)
