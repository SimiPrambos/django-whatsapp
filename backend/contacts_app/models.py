from enum import Enum
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from numbers_app.models import WhatsappNumbers
import phonenumbers

class GenderChoices(Enum):
    M = 'Man'
    W = 'Woman'
    O = 'Other'


class Contacts(models.Model):
    class Meta:
        db_table = 'contacts'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50, blank=True, null=True)
    number = models.CharField(max_length=50)
    country = models.CharField(max_length=3)
    is_whatsapp_number = models.BooleanField(default=False)
    is_phone_number = models.BooleanField(default=False)
    
    # opsional
    gender = models.CharField(
        max_length=1, 
        choices=[(tag.name, tag.value) for tag in GenderChoices],
        default='O'
    )
    location = models.CharField(max_length=50, blank=True, null=True)
    profession = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)


    def __str__(self):
        return self.number
    
    @property
    def get_chatid(self):
        return self.number+'@c.us' if not '@c.us' in self.number else self.number


@receiver(signal=post_save, sender=Contacts)
def validating_phone_number(sender, instance, created, **kwargs):
    if created:
        phone = instance.number
        is_valid = False
        try:
            parsed = phonenumbers.parse(phone, instance.country.upper())
            is_valid = phonenumbers.is_valid_number(parsed)
            if is_valid:
                phone = parsed
        except:
            pass
        instance.number = phone
        instance.is_phone_number = is_valid
        instance.save()