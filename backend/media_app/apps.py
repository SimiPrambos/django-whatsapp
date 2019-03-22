from django.apps import AppConfig


class MediaAppsConfig(AppConfig):
    name = 'media_app'

    def ready(self):
        import media_app.signals