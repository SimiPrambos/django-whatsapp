from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..serializers.media import UsersMediaSerializer
from media_app.models import UsersMedia

class UsersMediaViewset(viewsets.ModelViewSet):
    queryset = UsersMedia.objects.all()
    serializer_class = UsersMediaSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super(UsersMediaViewset, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)