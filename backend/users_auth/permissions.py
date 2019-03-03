from datetime import datetime
from rest_framework import permissions, exceptions
from .models import UsersAuth
from driver_manager.drivers import status_instance

class HasAPIAccess(permissions.BasePermission):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')
        status = UsersAuth.objects.filter(
                    api_key=api_key,
                    expired__gt=datetime.now().date()
                    ).exists()
        if not status:
            raise exceptions.PermissionDenied(self.message)
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