from rest_framework import serializers
from messages_app.models import WhatsappChatMessages, WhatsappMediaMessages, FriendMessages
from .media import UsersMediaSerializer
from django.template import Template, Context

class JSONSerializerField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class WhatsappChatSerializer(serializers.ModelSerializer):
    number = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    message_type = serializers.ReadOnlyField(default='OUT')
    template = JSONSerializerField(required=False)
    
    class Meta:
        model = WhatsappChatMessages
        fields = (
            'id', 'number', 'message_type', 'message_number',
            'message_content', 'message_status',
            'message_timestamp', 'template'
        )

    def validate(self, validated_data):
        template = validated_data.pop('template', None)
        if template:
            t = Template(validated_data.get('message_content'))
            c = Context(template)
            validated_data['message_content'] = t.render(c)
        return validated_data

class WhatsappMediaSerializer(serializers.ModelSerializer):
    number = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    message_type = serializers.ReadOnlyField(default='OUT')
    template = JSONSerializerField(required=False)

    class Meta:
        model = WhatsappMediaMessages
        fields = fields = (
            'id', 'number', 'message_type', 'message_number',
            'message_media', 'message_content', 'message_status',
            'message_timestamp', 'template'
        )

    def validate(self, validated_data):
        template = validated_data.pop('template', None)
        if template:
            t = Template(validated_data.get('message_content'))
            c = Context(template)
            validated_data['message_content'] = t.render(c)
        return validated_data

class FriendMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendMessages
        exclude = ('user',)