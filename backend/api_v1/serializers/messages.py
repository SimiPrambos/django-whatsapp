from rest_framework import serializers
from messages_app.models import WhatsappChatMessages, WhatsappMediaMessages
from .media import UsersMediaSerializer

class WhatsappChatSerializer(serializers.ModelSerializer):
    number = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    message_type = serializers.ReadOnlyField(default='OUT')
    
    class Meta:
        model = WhatsappChatMessages
        fields = '__all__'


class WhatsappMediaSerializer(serializers.ModelSerializer):
    number = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    message_type = serializers.ReadOnlyField(default='OUT')

    class Meta:
        model = WhatsappMediaMessages
        fields = '__all__'