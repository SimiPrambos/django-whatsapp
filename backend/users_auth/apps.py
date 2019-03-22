from django.apps import AppConfig


class NumbersAppConfig(AppConfig):
    name = 'users_auth'

    def ready(self):
        import users_auth.signals