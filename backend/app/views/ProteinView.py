from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from factories.ProteinFactory import ProteinFactory
from serializers.ProteinSerializer import ProteinSerializer
from serializers.ErrorSerializer import ErrorSerializer


class ProteinView(APIView):
    @swagger_auto_schema(
        operation_summary="Returns protein by id",
        responses={200: ProteinSerializer(),
                   400: ErrorSerializer()})
    def get(self, request, pk, format=None):
        usecase = ProteinFactory.get_protein_usecase()
        try:
            protein = usecase.get_protein(pk)
            serializer = ProteinSerializer(protein)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise NotFound()
