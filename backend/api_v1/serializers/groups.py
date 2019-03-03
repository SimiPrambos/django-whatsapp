from rest_framework import serializers
from contacts_app.models import GroupContacts

class GroupContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupContacts
        fields = ('id', 'name')