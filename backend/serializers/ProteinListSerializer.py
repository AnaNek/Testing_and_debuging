from rest_framework import serializers
from serializers.ProteinSerializer import ProteinSerializer

class ProteinListSerializer(serializers.Serializer):
    infected = ProteinSerializer(many=True, read_only=True)
    uninfected = ProteinSerializer(many=True, read_only=True)
