from entities.ProfileEntity import ProfileEntity
from entities.SessionEntity import SessionEntity
from repositories.ProfileRepo import ProfileRepo

import jwt
from django.contrib import auth
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.contrib.auth.models import User
from backend import settings

import logging
logger = logging.getLogger(__name__)

class ProfileUsecase:
    def __init__(self, profile_repo):
        self.profile_repo = profile_repo

    def get_profile(self, username) -> ProfileEntity:
        profile = self.profile_repo.get(username)
        return profile

    def create_profile(self, username, password):
        user = User.objects.filter(username=username).first()
        if user:
            return None
        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.save()
        profile = ProfileEntity()
        profile.set(username, password)
        return self.profile_repo.create(profile)

    def create_session(self, username, password) -> SessionEntity:
        user = auth.authenticate(
            username=username,
            password=password
        )
        if user is None:
            return None

        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        session = SessionEntity()

        session.set(
            id=user.id,
            token=token,
            username=user.username
        )

        return session

    def verify_token(self, token) -> SessionEntity:
        data = {'token': token}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        username_by_token = valid_data['user'].username
        user = User.objects.filter(username=username_by_token).first()
        if user is None:
            return None
        session = SessionEntity()
        session.set(user.id, token, username_by_token)
        return session

    def update_profile(self, username, password) -> ProfileEntity:
        user = User.objects.filter(username=username).first()
        if user is None:
            return None
        user.set_password(password)
        user.save()
        profile = ProfileEntity()
        profile.set(username, password)
        return self.profile_repo.update(profile)
