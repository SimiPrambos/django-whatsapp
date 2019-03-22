import requests, json
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from .models import Setting, Webhook

@receiver(signal=post_save, sender=User)
def create_setting(sender, instance, created, **kwargs):
    if created:
        Setting.objects.create(user_id=instance.id)

@receiver(signal=pre_save, sender=Webhook)
def start_hook(sender, instance, **kwargs):
    if instance.setting.webhook_enable and instance.setting.webhook_url:
        payload = dict(
            event=instance.event,
            data=json.loads(instance.data)
        )
        headers = {
            "Content-Type":"application/json",
            "accept":"application/json"
        }
        response = requests.post(
            instance.setting.webhook_url,
            headers=headers,
            data=json.dumps(payload)
        )

        instance.status = response.status_code
    else:
        instance.delete()