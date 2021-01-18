from rest_framework import serializers
from serializers.OrganismSerializer import OrganismSerializer

class OrganismListSerializer(serializers.Serializer):
    organisms = OrganismSerializer(many=True, read_only=True)
