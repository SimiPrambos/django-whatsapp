from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from driver_manager.drivers import status_number
from numbers_app.models import WhatsappNumbers

class GroupContacts(models.Model):
    class Meta:
        db_table = 'group_contacts'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "{}: {}".format(self.id, self.name)


class Contacts(models.Model):
    class Meta:
        db_table = 'contacts'

    group = models.ForeignKey(GroupContacts, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50, blank=True, null=True)
    number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.number
    
    @property
    def get_chatid(self):
        return self.number+'@c.us' if not '@c.us' in self.number else self.number

# auto check status whatsapp number
# @receiver(pre_save, sender=Contacts)
# def checking_number(sender, instance, **kwargs):
#     status = False
#     try:
#         status = status_number(instance.wa_number ,instance.get_chatid)
#     except:
#         pass
#     instance.status = status