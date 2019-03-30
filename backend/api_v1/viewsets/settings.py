
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers.settings import SettingSerializer, WebhookSerializer
from users_setting.models import Setting, Webhook


class SettingViewset(generics.RetrieveUpdateAPIView):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().get(user_id=request.user.id)
        serializer = SettingSerializer(queryset, many=False)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_queryset().get(user_id=request.user.id)
        print(instance)
        serializer = SettingSerializer(instance, data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)