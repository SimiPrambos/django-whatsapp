import json
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import WhatsappChatMessages
from users_setting.models import Setting, Webhook

@receiver(signal=post_save, sender=WhatsappChatMessages)
def creating_hook(sender, instance, created, **kwargs):
    if created:
        instance.message_number = instance.get_number
        setting = Setting.objects.get(user_id=instance.number.user.id)
        if instance.message_type == 'IN' and (setting.webhook_enable and setting.webhook_url):
            Webhook.objects.create(
                setting_id=setting.id,
                event="Inbox",
                data=json.dumps({
                    "from":instance.get_number,
                    "content":instance.message_content,
                    "timestamp":instance.message_timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
                    "status":instance.message_status
                })
            )
        instance.save()