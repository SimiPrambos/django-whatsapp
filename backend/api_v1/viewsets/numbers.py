from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.response import Response

from ..serializers.numbers import NumbersSerializer, NumberSettingsSerializer

from numbers_app.models import WhatsappNumbers, NumberSettings

from driver_manager.drivers import start_instance, stop_instance, status_instance, get_instance

from users_auth.permissions import HasAPIAccess

class NumbersViewset(generics.ListCreateAPIView):
    queryset = WhatsappNumbers.objects.all()
    serializer_class = NumbersSerializer
    permission_classes = (HasAPIAccess, )

    def perform_create(self, serializer):
        user = User.objects.get(api_key__api_key=self.request.apikey)
        serializer.save(user_id=user.id)

    def get(self, request):
        queryset = self.get_queryset().filter(user__api_key__api_key=request.apikey).order_by('created_at')
        serializer = NumbersSerializer(queryset, many=True)
        return Response(serializer.data)


class DetailNumbersViewset(generics.RetrieveUpdateDestroyAPIView):
    queryset = WhatsappNumbers.objects.all()
    serializer_class = NumbersSerializer
    lookup_field = 'pk'
    permission_classes = (HasAPIAccess, )

    def get_queryset(self):
        queryset = super(DetailNumbersViewset, self).get_queryset()
        queryset = queryset.filter(
            user__api_key__api_key=self.request.apikey,
            id=self.kwargs['pk']    
        )
        return queryset


class NumberSettingsViewset(generics.RetrieveUpdateAPIView):
    queryset = NumberSettings.objects.all()
    serializer_class = NumberSettingsSerializer
    lookup_field = 'pk'
    permission_classes = (HasAPIAccess, )

    def get_queryset(self):
        queryset = super(NumberSettingsViewset, self).get_queryset()
        queryset = queryset.filter(
            number__user__api_key__api_key=self.request.apikey,
            number_id=self.kwargs['pk']    
        )
        return queryset


class StartNumber(generics.RetrieveAPIView):
    queryset = WhatsappNumbers.objects.all()
    serializer_class = NumbersSerializer
    lookup_field = 'pk'
    permission_classes = (HasAPIAccess, )

    def get(self, request, pk):
        queryset = self.get_queryset().filter(user__api_key__api_key=request.apikey, pk=pk)
        if not queryset.exists():
            return Response(status=404)
        is_running = False
        try:
            number_instance = start_instance(pk)
            is_running = True
        except:
            pass
        return Response({"running":is_running})


class StopNumber(generics.RetrieveAPIView):
    queryset = WhatsappNumbers.objects.all()
    serializer_class = NumbersSerializer
    lookup_field = 'pk'
    permission_classes = (HasAPIAccess, )

    def get(self, request, pk):
        queryset = self.get_queryset().filter(user__api_key__api_key=request.apikey, pk=pk)
        if not queryset.exists():
            return Response(status=404)
        is_running = stop_instance(pk)
        return Response({"running":not is_running})


class StatusNumber(generics.RetrieveAPIView):
    queryset = WhatsappNumbers.objects.all()
    serializer_class = NumbersSerializer
    lookup_field = 'pk'
    permission_classes = (HasAPIAccess, )

    def get(self, request, pk):
        queryset = self.get_queryset().filter(user__api_key__api_key=request.apikey, pk=pk)
        if not queryset.exists():
            return Response(status=404)
        number_status = status_instance(pk)
        return Response(number_status)


class LoginNumber(generics.RetrieveAPIView):
    queryset = WhatsappNumbers.objects.all()
    serializer_class = NumbersSerializer
    lookup_field = 'pk'
    permission_classes = (HasAPIAccess, )
    
    def get(self, request, pk):
        queryset = self.get_queryset().filter(user__api_key__api_key=request.apikey, pk=pk)
        if not queryset.exists():
            return Response(status=404)
        status = status_instance(pk)
        if status["is_running"]:
            if not status["is_logged_in"]:
                return Response({"qrcode":get_instance(pk).get_qr_base64()})
            else:
                return Response({"status":"isLoggedIn"})
        else:
            return Response({"status":"NotRunning"})