from django.contrib import admin
from .models import Contacts, ContactsCategory

admin.site.register(ContactsCategory)
admin.site.register(Contacts)