import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

def user_directory_path(instance, filename):
    filename = instance.filename + '.' + filename.rsplit('.')[-1]
    return '/'.join([str(instance.user.id), str(instance.created), filename])

class UsersMedia(models.Model):
    class Meta:
        db_table = 'user_media'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_media')
    created = models.DateField(auto_now_add=True)
    filename = models.CharField(max_length=100)
    filepath = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return self.filename


@receiver(post_delete, sender=UsersMedia)
def on_file_deleted(sender, instance, **kwargs):
    instance.filepath.delete(False)

@receiver(pre_save, sender=UsersMedia)
def on_file_updated(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).filepath
    except sender.DoesNotExist:
        return False
    
    if not old_file == instance.filepath:
        old_file.delete(False)