from rest_framework import serializers

class PatternSerializer(serializers.Serializer):
    hash = serializers.CharField()
    subsequence = serializers.CharField()
    start_pos = serializers.IntegerField()
    end_pos = serializers.IntegerField()
    id = serializers.IntegerField(read_only=True)
    
