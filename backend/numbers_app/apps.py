from django.apps import AppConfig


class NumbersAppConfig(AppConfig):
    name = 'numbers_app'

    def ready(self):
        import numbers_app.signals