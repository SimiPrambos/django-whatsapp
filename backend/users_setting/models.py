from enum import Enum
from django.db import models
from django.contrib.auth.models import User


class Setting(models.Model):
    class Meta:
        db_table = 'settings'

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class EventType(Enum):
    I = "Inbox"
    O = "Outbox"


class Webhook(models.Model):
    class Meta:
        db_table = 'webhooks'

    # user
    active = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)
