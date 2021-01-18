from django.test import TestCase
from django.contrib.auth.models import User
from repositories.ProfileRepo import ProfileRepo
from usecases.ProfileUsecase import ProfileUsecase
from entities.ProfileEntity import ProfileEntity
from entities.SessionEntity import SessionEntity
from unittest.mock import patch
import jwt
from django.contrib import auth
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

class MockProfileRepo(ProfileRepo):
    def __init__(self):
        self._profile = None
        self._count_get = 0
        self._count_update = 0
        self._count_create = 0

    @property
    def count_get(self):
        return self._count_get

    @property
    def count_update(self):
        return self._count_update

    @property
    def count_create(self):
        return self._count_create

    @property
    def profile(self):
        return self._profile

    def get(self, username):
        self._count_get += 1
        return ProfileEntity(username=username)

    def update(self, profile):
        self._count_update += 1
        self._profile = profile
        return profile

    def create(self, profile):
        self._count_create += 1
        self._profile = profile
        return profile


class TestProfileUsecase(TestCase):

    def test_get_profile(self):
        # Arrange
        username = "somename"
        mock = MockProfileRepo()
        usecases = ProfileUsecase(mock)

        # Act
        profile = usecases.get_profile(username)

        # Assert
        self.assertEqual(profile.username, username)
        self.assertEqual(mock.count_get, 1)

    def test_create_profile(self):
        # Arrange
        username = "somename"
        password = "somepassword"
        expected_count = 1
        mock = MockProfileRepo()
        usecases = ProfileUsecase(mock)

        # Act
        profile = usecases.create_profile(username, password)

        # Assert
        self.assertEqual(mock.count_create, 1)

    def test_update_profile(self):
        # Arrange
        username = "somename"
        password = "somepassword"
        new_password = "new_password"
        user = User.objects.create_user(
            username=username,
            password=password
        )
        mock = MockProfileRepo()
        usecases = ProfileUsecase(mock)

        # Act
        profile = usecases.update_profile(username, new_password)

        # Assert
        self.assertEqual(mock.count_update, 1)

    @patch("jwt.encode")
    def test_create_session(self, mock_jwt):
        # Arrange
        username = "somename"
        password = "somepassword"
        token = "sometoken"
        mock_jwt.return_value = token
        user = User.objects.create_user(
            username=username,
            password=password
        )
        expected_session = SessionEntity(id=user.id, username=username, token=token).__dict__
        mock = MockProfileRepo()
        usecases = ProfileUsecase(mock)

        # Act
        session = usecases.create_session(username, password)
        actual_session = session.__dict__

        # Assert
        self.assertDictEqual(expected_session, actual_session)

    @patch("rest_framework_jwt.serializers.VerifyJSONWebTokenSerializer.validate")
    def test_verify_token(self, mock_jwt):
        # Arrange
        username = "somename"
        password = "somepassword"
        token = "sometoken"
        data = {"token":token}
        user = User.objects.create_user(
            username=username,
            password=password
        )
        expected_session = SessionEntity(id=user.id, username=username, token=token).__dict__
        mock_jwt.return_value = {'user':user}
        mock = MockProfileRepo()
        usecases = ProfileUsecase(mock)

        # Act
        session = usecases.verify_token(token)
        actual_session = session.__dict__

        # Arrange
        self.assertDictEqual(expected_session, actual_session)
        mock_jwt.assert_called_once_with(data)
