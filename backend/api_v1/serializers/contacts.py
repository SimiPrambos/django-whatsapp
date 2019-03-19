from rest_framework import serializers
from contacts_app.models import Contacts



class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        exclude = ['user']