from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from factories.ResultFactory import ResultFactory
from serializers.ResultSerializer import ResultSerializer
from serializers.ErrorSerializer import ErrorSerializer

import logging
logger = logging.getLogger(__name__)

class ResultView(APIView):
    @swagger_auto_schema(
        operation_summary="Returns patterns by pair of protein ids",
        responses={200: ResultSerializer(),
                   400: ErrorSerializer()})
    def get(self, request, pk1, pk2, format=None):
        usecase = ResultFactory.get_result_usecase()
        try:
            result = usecase.get_result(pk1, pk2)

            if result is None:
                usecase.create_result(pk1, pk2, None)
                result = usecase.get_result(pk1, pk2)
            serializer = ResultSerializer(result)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise NotFound("not found")
