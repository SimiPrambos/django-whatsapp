from django.contrib import admin
from .models import WhatsappChatMessages, WhatsappMediaMessages, FriendMessages

admin.site.register(WhatsappChatMessages)
admin.site.register(WhatsappMediaMessages)
admin.site.register(FriendMessages)