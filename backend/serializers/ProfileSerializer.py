from rest_framework import serializers

class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
