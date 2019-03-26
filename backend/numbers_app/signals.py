from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from driver_manager.drivers import delete_client
from .models import WhatsappNumbers, NumberSettings

@receiver(post_delete, sender=WhatsappNumbers)
def on_number_delete(sender, instance, **kwargs):
    delete_client(instance.id, remove_cache=True)

@receiver(post_save, sender=WhatsappNumbers)
def create_number_setting(sender, instance, created, **kwargs):
    if created:
        NumberSettings.objects.create(number_id=instance.id)