from datetime import time
from django.db import models
from django.contrib.auth import get_user_model
from driver_manager.drivers import status_instance

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


class NumberSettings(models.Model):
    class Meta:
        db_table = 'number_settings'

    number = models.OneToOneField('numbers_app.WhatsappNumbers', on_delete=models.CASCADE)
    record_inbox = models.BooleanField(default=True)
    auto_read = models.BooleanField(default=True)
    max_delay = models.IntegerField(default=20)
    auto_reboot = models.TimeField(default=time(00,00))
    send_schedule_from = models.TimeField(default=time(00,30))
    send_schedule_to = models.TimeField(default=time(23,30))

    def __str__(self):
        return self.number.lable