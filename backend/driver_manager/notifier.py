import threading

class HandleReceivedMessage(threading.Thread):
    def __init__(self, id, messages_obj):
        self.id = id
        self.messages = messages_obj
        self.deamon = True
        threading.Thread.__init__(self)

    def run(self):
        for messages in self.messages:
            for message in messages.messages:
                if message.type == 'chat':
                    self.record_message(
                        self.id,
                        message.sender.id,
                        message.content,
                        message.timestamp
                    )
    
    def record_text_message(self, id, sender, content, received):
        from messages_app.models import WhatsappChatMessages
        WhatsappChatMessages(
            number_id=id,
            message_type="IN",
            message_number=sender,
            message_content=content,
            message_status=True,
            message_timestamp=received
        ).save()


class HandleSendMessage(threading.Thread):
    def __init__(self, id, instance, media=False, **message):
        self.id = id
        self.instance = instance
        self.media = media
        self.message = message
        self.deamon = True
        threading.Thread.__init__(self)

    def run(self):
        if self.media:
            self.send_media_message(
                self.id,
                self.message['to'],
                self.message['caption'],
                self.message['file']
            )
        else:
            self.send_text_message(
                self.id,
                self.message['to'],
                self.message['content']
            )
    
    def send_text_message(self, id, to, content):
        from .drivers import send_message, status_number

        if not self.validate(id, to):
            return
        self.instance.message_status = send_message(id, to, content)
        self.instance.save()

    def send_media_message(self, id, to, caption, media):
        from .drivers import send_media

        if not self.validate(id, to):
            return
        self.instance.message_status = send_media(id, to, caption, media)
        self.instance.save()

    def validate(self, id, number):
        from .drivers import status_number

        return status_number(id, number)


class HandleValidateNumber(threading.Thread):
    def __init__(self, id, instances):
        self.id = id
        self.instances = instances
        self.deamon = True
        threading.Thread.__init__(self)

    def run(self):
        for instance in self.instances:
            self.validate(self.id, intance)

    def validate(self, id, intance):
        from .drivers import status_number

        intance.is_active = status_number(id, intance.get_chatid)
        intance.save()
        