from enum import Enum
from django.db import models
from django.contrib.auth.models import User

def get_chatid(number):
    return number+'@c.us' if not '@c.us' in number else number

def get_number(chatid):
    return chatid.replace('@c.us', '') if '@c.us' in chatid else chatid

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
    send_retry = models.IntegerField(default=0)
    on_progress = models.BooleanField(default=False)

    @property
    def get_chatid(self):
        return get_chatid(self.message_number)

    @property
    def get_number(self):
        return get_number(self.message_number)

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
    send_retry = models.IntegerField(default=0)
    on_progress = models.BooleanField(default=False)

    @property
    def get_chatid(self):
        return get_chatid(self.message_number)

    def __str__(self):
        return self.message_number


class FriendMessages(models.Model):
    class Meta:
        db_table = 'friend_messages'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.message