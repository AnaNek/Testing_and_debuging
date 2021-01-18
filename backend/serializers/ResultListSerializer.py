from rest_framework import serializers
from serializers.ResultSerializer import ResultSerializer

class ResultListSerializer(serializers.Serializer):
    results = ResultSerializer(many=True, read_only=True)
