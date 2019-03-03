from rest_framework import serializers
from media_app.models import UsersMedia

class UsersMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersMedia
        fields = ('id', 'filename', 'filepath', 'created')