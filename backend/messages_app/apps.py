from django.apps import AppConfig


class MessagesAppConfig(AppConfig):
    name = 'messages_app'

    def ready(self):
        import messages_app.signals