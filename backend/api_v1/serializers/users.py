from rest_framework import serializers
from django.contrib.auth.models import User

class UsersSerializer(serializers.ModelSerializer):
    api_expired = serializers.StringRelatedField(source='api_key.expired', many=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active', 'is_superuser', 'api_expired')