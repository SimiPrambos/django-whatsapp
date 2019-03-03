from django.contrib import admin
from .models import WhatsappChatMessages, WhatsappMediaMessages

admin.site.register(WhatsappChatMessages)
admin.site.register(WhatsappMediaMessages)