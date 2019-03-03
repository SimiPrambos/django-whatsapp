from enum import Enum
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from driver_manager.notifier import HandleSendMessage

def get_chatid(number):
    return number+'@c.us' if not '@c.us' in number else number

class MessageType(Enum):
    IN = 'Inbox'
    OUT = 'Outbox'


class MessageStatus(Enum):
    P = 'Pending'
    D = 'Delivered'
    F = 'Failed'
    

class WhatsappChatMessages(models.Model):
    class Meta:
        db_table = 'chat_messages'
    number = models.ForeignKey('numbers_app.WhatsappNumbers', on_delete=models.CASCADE, related_name='whatsapp_chat')
    message_type = models.CharField(max_length=3, choices=[(tag.name, tag.value) for tag in MessageType])
    message_number = models.CharField(max_length=25)
    message_content = models.TextField(blank=True, null=True)
    message_status = models.CharField(max_length=1, choices=[(tag.name, tag.value) for tag in MessageStatus], default='P')
    message_timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_chatid(self):
        return get_chatid(self.message_number)

    def __str__(self):
        return self.message_number

class WhatsappMediaMessages(models.Model):
    class Meta:
        db_table = 'media_messages'
    number = models.ForeignKey('numbers_app.WhatsappNumbers', on_delete=models.CASCADE, related_name='whatsapp_media')
    message_type = models.CharField(max_length=3, choices=[(tag, tag.value) for tag in MessageType])
    message_number = models.CharField(max_length=25)
    message_media = models.ForeignKey('media_app.UsersMedia', on_delete=models.CASCADE)
    message_content = models.TextField(blank=True, null=True)
    message_status = models.CharField(max_length=1, choices=[(tag.name, tag.value) for tag in MessageStatus], default='P')
    message_timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def get_chatid(self):
        return get_chatid(self.message_number)

    def __str__(self):
        return self.message_number

@receiver(post_save, sender=WhatsappChatMessages)
def sending_text_message(sender, instance, created, **kwargs):
    if created and instance.message_type == 'OUT':
        HandleSendMessage(
            id=instance.number.id,
            instance=instance,
            media=False,
            **dict(
                to=instance.get_chatid,
                content=instance.message_content
            )
        ).start()

@receiver(post_save, sender=WhatsappMediaMessages)
def sending_media_message(sender, instance, created, **kwargs):
    if created and instance.message_type == 'OUT':
        HandleSendMessage(
            id=instance.number.id,
            instance=instance,
            media=True,
            **dict(
                to=instance.get_chatid,
                caption=instance.message_content,
                file=instance.message_media.filepath.path
            )
        ).start()