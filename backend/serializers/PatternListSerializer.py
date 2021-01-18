from rest_framework import serializers
from serializers.PatternSerializer import PatternSerializer

class PatternListSerializer(serializers.Serializer):
    patterns = PatternSerializer(many=True, read_only=True)
