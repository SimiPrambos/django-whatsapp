from rest_framework import serializers
from djoser.serializers import CurrentUserSerializer

class CustomUserSerializer(CurrentUserSerializer):
    api_key = serializers.StringRelatedField(source="api_key.api_key", many=False)
    expired = serializers.StringRelatedField(source="api_key.expired", many=False)
    was_expired = serializers.BooleanField(source="api_key.was_expired")

    class Meta(CurrentUserSerializer.Meta):
        fields = ("id", "username", "email", "api_key", "date_joined", "expired", "is_active", "is_superuser", "was_expired")