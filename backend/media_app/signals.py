from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from .models import UsersMedia

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