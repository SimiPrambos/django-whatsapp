from rest_framework import serializers
from users_setting.models import Setting, Webhook

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        exclude = ["user"]


class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        exclude = ["setting"]