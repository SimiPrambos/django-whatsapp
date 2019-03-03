from django.db import models
from django.contrib.auth.models import User
from .helpers import generate_key
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

class UsersAuth(models.Model):
    class Meta:
        db_table = 'users_auth'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_key')
    created = models.DateTimeField(auto_now_add=True)
    expired = models.DateField()
    api_key = models.CharField(max_length=40, unique=True, default=generate_key)

    def save(self, *args, **kwargs):
        if not self.api_key:
            key = generate_key()
            self.api_key = key
        super(UsersAuth, self).save(*args, **kwargs)

    def __str__(self):
        return self.api_key

@receiver(post_save, sender=User)
def create_apikey(sender, instance, **kwargs):
    userauth = UsersAuth.objects.filter(user_id=instance.id)
    if not userauth.exists():
        UsersAuth.objects.create(
            user_id=instance.id,
            expired=datetime.now() + timedelta(days=30))