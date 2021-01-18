from rest_framework import serializers

class SessionSerializer(serializers.Serializer):
    username = serializers.CharField()
    token = serializers.CharField()
    id = serializers.IntegerField()
