import threading

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class HandleReceivedMessage(threading.Thread):
    def __init__(self, id, messages_obj):
        self.id = id
        self.messages = messages_obj
        # self.deamon = True
        threading.Thread.__init__(self)

    def run(self):
        for messages in self.messages:
            for message in messages.messages:
                if message.type == 'chat':
                    self.record_text_message(
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
            message_status='D',
            message_timestamp=received
        ).save()


class HandleSendMessage(threading.Thread):
    def __init__(self, id, instance, media=False):
        self.id = id
        self.instance = instance
        self.media = media
        self.status = None
        # self.deamon = True
        print("thread send to ", instance.get_chatid)
        threading.Thread.__init__(self)

    def run(self):
        self.instance.on_progress = True
        self.instance.save()

        if self.media:
            self.send_media_message(
                id=self.id,
                to=self.instance.get_chatid,
                caption=self.instance.message_content,
                filepath=self.instance.message_media.filepath.path,
                instance=self.instance
            )
        else:
            self.send_text_message(
                id=self.id, 
                to=self.instance.get_chatid,
                content=self.instance.message_content,
                instance=self.instance
            )

        self.instance.message_status = self.status
        self.instance.send_retry += 1
        # self.instance.on_progress = False
        self.instance.save()

    def send_text_message(self, id, to, content, instance):
        from .drivers import send_message, status_number

        if not self.validate(id, to):
            return
        self.status = send_message(id, to, content)

    def send_media_message(self, id, to, caption, filepath, instance):
        from .drivers import send_media

        if not self.validate(id, to):
            return
        self.status = send_media(id, to, caption, filepath)

    def validate(self, id, number):
        from .drivers import status_number

        return status_number(id, number)


class HandleValidateNumber(threading.Thread):
    def __init__(self, id, instances):
        self.id = id
        self.instances = instances
        # self.deamon = True
        threading.Thread.__init__(self)

    def run(self):
        for instance in self.instances:
            self.validate(self.id, intance)

    def validate(self, id, intance):
        from .drivers import status_number

        intance.is_active = status_number(id, intance.get_chatid)
        intance.save()
        