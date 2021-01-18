from rest_framework import serializers
from serializers.OrganismSerializer import OrganismSerializer

class ProteinSerializer(serializers.Serializer):
    hash = serializers.CharField()
    sequence = serializers.CharField()
    organism = OrganismSerializer(read_only=True, required=False)
    id = serializers.IntegerField(read_only=True)
