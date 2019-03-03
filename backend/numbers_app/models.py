from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete
from driver_manager.drivers import status_instance, delete_client

def get_status(id):
    return status_instance(id)

class WhatsappNumbers(models.Model):
    class Meta:
        db_table = 'whatsapp_numbers'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
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