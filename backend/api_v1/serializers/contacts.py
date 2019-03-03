from rest_framework import serializers
from contacts_app.models import Contacts, GroupContacts
from .groups import GroupContactsSerializer

class ContactsSerializer(serializers.ModelSerializer):
    # group = serializers.PrimaryKeyRelatedField(queryset=GroupContacts.objects.all())
    class Meta:
        model = Contacts
        fields = ('id', 'name', 'number', 'is_active', 'group')
        # read_only_fields = ('is_active',)


class ValidateContactsSerializer(serializers.Serializer):
    number_id = serializers.IntegerField(write_only=True)