from django.apps import AppConfig


class UsersSettingConfig(AppConfig):
    name = 'users_setting'

    def ready(self):
        import users_setting.signals