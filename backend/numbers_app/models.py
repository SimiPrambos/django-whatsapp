from datetime import time
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from driver_manager.drivers import status_instance, delete_client

def get_status(id):
    return status_instance(id)

class WhatsappNumbers(models.Model):
    class Meta:
        db_table = 'whatsapp_numbers'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    lable = models.CharField(max_length=25)
    number = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def it_is_running(self):
        return get_status(self.id)['is_running']

    @property
    def it_is_logged_in(self):
        return get_status(self.id)['is_logged_in']

    def __str__(self):
        return self.lable


@receiver(post_delete, sender=WhatsappNumbers)
def on_number_delete(sender, instance, **kwargs):
    delete_client(instance.id, remove_cache=True)


class NumberSettings(models.Model):
    class Meta:
        db_table = 'number_settings'

    number = models.OneToOneField('numbers_app.WhatsappNumbers', on_delete=models.CASCADE)
    record_inbox = models.BooleanField(default=False)
    auto_read = models.BooleanField(default=True)
    max_delay = models.IntegerField(default=10)
    auto_reboot = models.TimeField(default=time(00,00))
    send_schedule_from = models.TimeField(default=time(00,30))
    send_schedule_to = models.TimeField(default=time(23,30))

    def __str__(self):
        return self.number.lable


@receiver(post_save, sender=WhatsappNumbers)
def create_number_setting(sender, instance, created, **kwargs):
    if created:
        NumberSettings.objects.create(number_id=instance.id)