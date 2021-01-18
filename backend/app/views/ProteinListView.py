from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import NotAuthenticated, ParseError, NotFound, PermissionDenied
from drf_yasg.utils import swagger_auto_schema

from factories.ProteinFactory import ProteinFactory
from factories.ProfileFactory import ProfileFactory
from serializers.ProteinListSerializer import ProteinListSerializer
from serializers.ProteinSerializer import ProteinSerializer
from serializers.ErrorSerializer import ErrorSerializer

import logging
logger = logging.getLogger(__name__)

class ProteinListView(APIView):
    @swagger_auto_schema(
        operation_summary="Returns all proteins",
        responses={200: ProteinListSerializer(),
                   400: ErrorSerializer()})
    def get(self, request, format=None):
        usecase = ProteinFactory.get_protein_usecase()
        infected = usecase.get_infected()
        uninfected = usecase.get_uninfected()

        proteins_serializer = {
            'infected': infected,
            'uninfected': uninfected
        }
        serializer = ProteinListSerializer(proteins_serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create protein",
        responses={200: ProteinSerializer(),
                   400: ErrorSerializer(),
                   401: ErrorSerializer()},
        request_body=ProteinSerializer())
    def post(self, request, format=None):
        token = request.session.get('token', False)
        if token == False:
            raise NotAuthenticated(detail='User is not authenticated', code="401")

        usecase = ProfileFactory.get_profile_usecase()
        session = usecase.verify_token(token)
        
        if session is None:
            raise NotFound()

        if not request.data.get('organism', False) or \
        not request.data.get('sequence', False):
            raise ParseError(detail="Not enought data")

        usecase = ProteinFactory.get_protein_usecase()
        protein = usecase.create_protein(request.data['sequence'],
                                         request.data['organism']['infected'],
                                         request.data['organism']['sex'],
                                         request.data['organism']['organism_mnemonic'],
                                         request.data['organism']['description'])
        serializer = ProteinSerializer(protein)
        return Response(serializer.data)
