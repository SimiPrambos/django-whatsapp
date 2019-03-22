import os
from django.db import models
from django.contrib.auth.models import User

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