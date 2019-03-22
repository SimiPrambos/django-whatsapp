from enum import Enum
from django.db import models
from django.contrib.auth.models import User


class Setting(models.Model):
    class Meta:
        db_table = 'settings'

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    webhook_enable = models.BooleanField(default=False)
    webhook_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Webhook(models.Model):
    class Meta:
        db_table = 'webhooks'

    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    event = models.CharField(max_length=50)
    data = models.TextField(max_length=50000, blank=True, null=True)
    status = models.IntegerField(default=400)

    def __str__(self):
        return self.event
