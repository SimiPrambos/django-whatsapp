from enum import Enum
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from numbers_app.models import WhatsappNumbers

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
    is_friend = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=1, 
        choices=[(tag.name, tag.value) for tag in GenderChoices],
        default='O', blank=True, null=True
    )
    location = models.CharField(max_length=50, blank=True, null=True)
    profession = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(default=timezone.now().date(), blank=True, null=True)
    additional = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.number)
    
    @property
    def get_chatid(self):
        return str(self.number)+'@c.us' if not '@c.us' in str(self.number) else str(self.number)