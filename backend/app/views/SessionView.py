from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from factories.ProfileFactory import ProfileFactory
from serializers.ErrorSerializer import ErrorSerializer
from serializers.TokenSerializer import TokenSerializer
from serializers.SessionSerializer import SessionSerializer
from serializers.ProfileSerializer import ProfileSerializer
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from rest_framework.exceptions import NotAuthenticated, ParseError, NotFound, PermissionDenied
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

import logging
logger = logging.getLogger(__name__)

class SessionView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Logout",
        responses={200: SessionSerializer(),
                   400: ErrorSerializer(),
                   403: ErrorSerializer()},
    )
    def delete(self, request, username, format=None):
        token = request.session.get('token', False)
        if token == False:
            raise NotAuthenticated(detail='User is not authenticated', code="401")

        usecase = ProfileFactory.get_profile_usecase()
        session = usecase.verify_token(token)

        if session is None:
            raise NotFound()

        if session.username != username:
            raise PermissionDenied()

        #logger.exception(request.session.get('token'))
        logout(request)

        serializer = SessionSerializer(session)
        return Response(serializer.data)
