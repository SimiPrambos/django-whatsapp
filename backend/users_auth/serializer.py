from rest_framework import serializers
from djoser.serializers import CurrentUserSerializer

class CustomUserSerializer(CurrentUserSerializer):
    api_key = serializers.StringRelatedField(many=False)

    class Meta(CurrentUserSerializer.Meta):
        fields = ("id", "username", "email", "api_key")