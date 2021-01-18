from rest_framework import serializers

class OrganismSerializer(serializers.Serializer):
    organism_mnemonic = serializers.CharField()
    infected = serializers.BooleanField()
    sex = serializers.CharField()
    description = serializers.CharField()
