from datetime import datetime
from rest_framework import permissions, exceptions
from .models import UsersAuth
from driver_manager.drivers import status_instance

class HasAPIAccess(permissions.BasePermission):
    invalid_api_key = 'Invalid or missing API Key.'
    expired_api_key = 'Api Key was expired'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')
        status = UsersAuth.objects.get(api_key=api_key)
        if not status:
            raise exceptions.PermissionDenied(self.invalid_api_key)
        if status.expired <= datetime.now().date():
            raise exceptions.PermissionDenied(self.expired_api_key)
        return status

class HasWhatsappLoggedIn(permissions.BasePermission):
    message = 'Whatsapp number is not logged in.'

    def has_permission(self, request, view):
        if request.method == 'POST':
            status = status_instance(view.kwargs['pk'])['is_logged_in']
            if not status:
                raise exceptions.PermissionDenied(self.message)
            return status
        else:
            return True