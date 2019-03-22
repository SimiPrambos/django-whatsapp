from django.contrib import admin
from .models import Setting, Webhook

admin.site.register(Setting)
admin.site.register(Webhook)