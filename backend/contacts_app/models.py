from enum import Enum
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from driver_manager.drivers import status_number
from numbers_app.models import WhatsappNumbers

class GenderChoices(Enum):
    M = 'Man'
    W = 'Woman'
    O = 'Other'


class ContactsCategory(models.Model):
    class Meta:
        db_table = 'category'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Contacts(models.Model):
    class Meta:
        db_table = 'contacts'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(to=ContactsCategory, related_name='contacts')
    
    name = models.CharField(max_length=50, blank=True, null=True)
    number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    
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


@receiver(signal=post_save, sender=User)
def create_default_category(sender, instance, created, **kwargs):
    if created:
        ContactsCategory.objects.create(
            user_id=instance.id,
            name="default"
        )