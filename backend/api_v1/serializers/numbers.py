# drf
from rest_framework import serializers

# numbers_app models
from numbers_app.models import WhatsappNumbers
from driver_manager.drivers import status_instance

class NumbersSerializer(serializers.ModelSerializer):
    is_running = serializers.ReadOnlyField(source='it_is_running')
    is_logged_in = serializers.ReadOnlyField(source='it_is_logged_in')

    class Meta:
        model = WhatsappNumbers
        fields = ('id', 'lable', 'number', 'created_at', 'is_running', 'is_logged_in')
