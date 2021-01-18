from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt, ensure_csrf_cookie
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotAuthenticated, ParseError, NotFound, PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login

from factories.ProfileFactory import ProfileFactory
from serializers.ErrorSerializer import ErrorSerializer
from serializers.ProfileSerializer import ProfileSerializer

import logging
logger = logging.getLogger(__name__)

class ProfileView(APIView):

    @swagger_auto_schema(
        operation_summary="Returns user's information",
        responses={200: ProfileSerializer(),
                   401: ErrorSerializer(),
                   404: ErrorSerializer(),
                   403: ErrorSerializer()},
    )
    @csrf_exempt
    def get(self, request, username, format=None):
        token = request.session.get('token', False)

        if token == False:
            raise NotAuthenticated(detail='User is not authenticated', code="401")

        usecase = ProfileFactory.get_profile_usecase()
        session = usecase.verify_token(token)

        if session is None:
            raise NotFound()

        if session.username != username:
            raise PermissionDenied()

        usecase = ProfileFactory.get_profile_usecase()
        profile = usecase.get_profile(username)

        if profile is None:
            raise NotFound(detail='user is not exist')

        serializer = ProfileSerializer(profile)

        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update user's info",
        responses={200: ProfileSerializer(),
                   401: ErrorSerializer(),
                   404: ErrorSerializer(),
                   403: ErrorSerializer()},
        request_body=ProfileSerializer()
    )
    def patch(self, request, username, format=None):
        token = request.session.get('token', False)
        if token == False:
            raise NotAuthenticated(detail='User is not authenticated', code="401")

        usecase = ProfileFactory.get_profile_usecase()
        session = usecase.verify_token(token)

        if session is None:
            raise NotFound()

        if session.username != username:
            raise PermissionDenied()

        usecase = ProfileFactory.get_profile_usecase()
        profile = usecase.update_profile(
            username,
            request.data.get('password', False)
        )

        if profile is None:
            raise NotFound(detail='user is not exist')

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
