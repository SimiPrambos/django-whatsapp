from rest_framework import serializers
from contacts_app.models import Contacts, ContactsCategory

class ContactsSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Contacts
        exclude = ['user']


class ContactsCategorySerializer(serializers.ModelSerializer):
    # contacts = ContactsSerializer(many=True, read_only=True, fields=['name'])
    class Meta:
        model = ContactsCategory
        fields = ['id', 'name']


class ValidateContactsSerializer(serializers.Serializer):
    number_id = serializers.IntegerField(write_only=True)