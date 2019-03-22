import phonenumbers
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Contacts

@receiver(signal=post_save, sender=Contacts)
def validating_phone_number(sender, instance, created, **kwargs):
    if created:
        phone = instance.number
        is_valid = False
        try:
            parsed = phonenumbers.parse(phone, str(instance.country).upper())
            is_valid = phonenumbers.is_valid_number(parsed)
            if is_valid:
                phone = "{}{}".format(parsed.country_code, parsed.national_number)
        except:
            pass
        instance.number = phone
        instance.is_phone_number = is_valid
        instance.save()