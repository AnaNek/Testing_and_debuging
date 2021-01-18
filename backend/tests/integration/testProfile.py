from django.test import TestCase, RequestFactory
from unittest.mock import patch, call
from django.contrib.auth.models import User
from usecases.ProfileUsecase import ProfileUsecase
from repositories.ProfileRepo import ProfileRepo
from entities.ProfileEntity import ProfileEntity
from entities.SessionEntity import SessionEntity
from app.views.ProfileView import ProfileView
from app.views.ProfileListView import ProfileListView
from models_db.Profile import Profile
from django.contrib.auth.models import User

class TestIntegrationViewUsecaseProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username='user', email='', 
            password='secret'
        )
    
    @patch("repositories.ProfileRepo.ProfileRepo.create")
    def test_post_profile(self, mock_repo):
        # Arrange
        username = 'someuser'
        password = 'password'
        expected_profile = ProfileEntity(username=username, password=password)
        mock_repo.return_value = expected_profile
        expected_status_code = 200
        expected_json = {'username': username, 'password': password}
        form_data = {
            'username': username,
            'password': password
        }
        request = self.factory.post('/users/', content_type='application/json', data=form_data)
        request.user = self.user

        # Act
        response = ProfileListView.as_view()(request)

        # Assert
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.data, expected_json)
        self.assertEqual(mock_repo.call_count, 1)

    @patch("repositories.ProfileRepo.ProfileRepo.get")
    @patch("usecases.ProfileUsecase.ProfileUsecase.verify_token")
    def test_get_profile(self, mock_verify, mock_repo):
        # Arrange
        username = 'someuser'
        password = 'password'
        expected_profile = ProfileEntity(username=username, password=password)
        mock_verify.return_value = SessionEntity(username=username)
        mock_repo.return_value = expected_profile
        expected_status_code = 200
        expected_json = {'username': username, 'password': password}
        url = '/users/' + str(username) + '/'
        request = self.factory.get(url)
        request.user = self.user
        request.session = {'token': 'sometoken'}

        # Act
        response = ProfileView.as_view()(request, username)

        # Assert
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.data, expected_json)
        self.assertEqual(mock_repo.call_count, 1)

    @patch("repositories.ProfileRepo.ProfileRepo.update")
    @patch("usecases.ProfileUsecase.ProfileUsecase.verify_token")
    def test_patch_profile(self, mock_verify, mock_repo):
        # Arrange
        username = self.user.username
        new_password = 'new_password'
        expected_profile = ProfileEntity(username=username, password=new_password)
        mock_verify.return_value = SessionEntity(username=username)
        mock_repo.return_value = expected_profile
        expected_status_code = 200
        expected_json = {'username': username, 'password': new_password}
        form_data = {
            'username': username,
            'password': new_password
        }
        url = '/users/' + str(username) + '/'
        request = self.factory.patch(url, content_type='application/json', data=form_data)
        request.user = self.user
        request.session = {'token': 'sometoken'}

        # Act
        response = ProfileView.as_view()(request, username)

        # Assert
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.data, expected_json)
        self.assertEqual(mock_repo.call_count, 1)


class TestIntegrationRepoUsecaseProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "username"
        cls.password = "password"
        user = User.objects.create_user(
            username=cls.username,
            password=cls.password
        )
        cls.profile = Profile.objects.create(username=cls.username, 
                                             password=cls.password)

    def test_create_profile(self):
        # Arrange
        username = "someone"
        password = "password"
        expected_profile = {'username':username, 'password':password}
        repo = ProfileRepo()
        usecases = ProfileUsecase(repo)

        # Act
        usecases.create_profile(username, password)
        profile = Profile.objects.all().filter(username=username).first()
        actual_profile = {'username':profile.username, 'password':profile.password}

        # Assert
        self.assertDictEqual(actual_profile, expected_profile)

    def test_update_profile(self):
        # Arrange
        username = self.username
        new_password = "new_password"
        expected_profile = {'username':username, 'password':new_password}
        repo = ProfileRepo()
        usecases = ProfileUsecase(repo)

        # Act
        profile = usecases.update_profile(username, new_password)
        profile = Profile.objects.all().filter(username=username).first()
        actual_profile = {'username':profile.username, 'password':profile.password}

        # Assert
        self.assertDictEqual(actual_profile, expected_profile)

    def test_get_profile(self):
        # Arrange
        username = self.username
        password = self.password
        expected_profile = {'username':username, 'password':password}
        repo = ProfileRepo()
        usecases = ProfileUsecase(repo)

        # Act
        profile = usecases.get_profile(username)
        actual_profile = {'username':profile.username, 'password':profile.password}

        # Assert
        self.assertDictEqual(actual_profile, expected_profile)
