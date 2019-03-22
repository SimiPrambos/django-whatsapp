from django.apps import AppConfig


class ContactsAppConfig(AppConfig):
    name = 'contacts_app'

    def ready(self):
        import contacts_app.signals