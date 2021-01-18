from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from factories.ProfileFactory import ProfileFactory
from serializers.ErrorSerializer import ErrorSerializer
from serializers.ProfileSerializer import ProfileSerializer


class ProfileListView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Create user",
        responses={200: ProfileSerializer(),
                   400: ErrorSerializer()},
        request_body=ProfileSerializer())
    def post(self, request):
        if (not request.data
                or not request.data.get('username', False)
                or not request.data.get('password', False)):
            raise ParseError(detail="No username and password")

        usecase = ProfileFactory.get_profile_usecase()
        user = usecase.create_profile(
            request.data['username'],
            request.data['password']
        )
        if user is None:
            raise ParseError(detail="invalid data")

        serializer = ProfileSerializer(user)
        return Response(serializer.data)
