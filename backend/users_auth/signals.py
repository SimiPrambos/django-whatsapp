from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UsersAuth

@receiver(post_save, sender=User)
def create_apikey(sender, instance, **kwargs):
    userauth = UsersAuth.objects.filter(user_id=instance.id)
    if not userauth.exists():
        UsersAuth.objects.create(
            user_id=instance.id,
            expired=datetime.now() + timedelta(days=30))