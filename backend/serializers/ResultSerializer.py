from rest_framework import serializers
from serializers.PatternSerializer import PatternSerializer
from serializers.PairSerializer import PairSerializer

class ResultSerializer(serializers.Serializer):
    pair = PairSerializer(read_only=True, required=False)
    patterns = PatternSerializer(many=True, read_only=True)
