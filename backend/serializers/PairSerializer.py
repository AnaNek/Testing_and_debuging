from rest_framework import serializers
from serializers.ProteinSerializer import ProteinSerializer

class PairSerializer(serializers.Serializer):
    protein1 = ProteinSerializer(read_only=True, required=False)
    protein2 = ProteinSerializer(read_only=True, required=False)
    similarity = serializers.FloatField()
    pattern_count = serializers.IntegerField()
    id = serializers.IntegerField(read_only=True)
