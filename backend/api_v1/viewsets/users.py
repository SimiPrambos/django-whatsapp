from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..serializers.users import UsersSerializer
from users_auth.models import UsersAuth

class UsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, IsAdminUser)

    @action(detail=True, methods=['PUT'])
    def set_expiration(self, request, pk=None):
        user = self.get_object()
        auth = UsersAuth.objects.get(pk=pk)
        serializer = UsersSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        auth.expired = request.data.get('api_expired')
        auth.save()
        return Response(serializer.data)