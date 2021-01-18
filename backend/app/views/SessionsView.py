from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from factories.ProfileFactory import ProfileFactory
from serializers.ErrorSerializer import ErrorSerializer
from serializers.SessionSerializer import SessionSerializer
from serializers.ProfileSerializer import ProfileSerializer
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login

import logging
logger = logging.getLogger(__name__)

class SessionsView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Login user",
        responses={200: SessionSerializer(),
                   400: ErrorSerializer(),
                   403: ErrorSerializer()},
        request_body=ProfileSerializer()
    )
    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        if not request.data \
                or not request.data.get('username', False) \
                or not request.data.get('password', False):
            raise ParseError(detail="Please provide username/password")

        usecase = ProfileFactory.get_profile_usecase()
        session = usecase.create_session(
             request.data.get('username', False),
             request.data.get('password', False)
        )

        if session is None:
            raise AuthenticationFailed()

        user = User.objects.filter(username=request.data.get('username', False)).first()
        login(request, user)

        request.session['token'] = session.token.decode()
        session.set_token(session.token.decode())
        serialized_session = SessionSerializer(session)
        return Response(serialized_session.data)
