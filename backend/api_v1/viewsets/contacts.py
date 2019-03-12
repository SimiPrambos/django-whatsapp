from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from ..serializers.contacts import ContactsCategorySerializer, ContactsSerializer, ValidateContactsSerializer
from contacts_app.models import Contacts, ContactsCategory
from users_auth.permissions import HasAPIAccess, HasWhatsappLoggedIn
from driver_manager.drivers import status_number
from numbers_app.models import WhatsappNumbers
from rest_framework_csv.parsers import CSVParser

class ContactsViewset(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super(ContactsViewset, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        category = serializer.validated_data.get('category') or []
        print(category)
        if not category:
            obj, created = ContactsCategory.objects.get_or_create(
                user_id=self.request.user.id,
                name='default'
            )
            category.append(obj.id)
        self.perform_create(serializer, category)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer, category):
        
        serializer.save(user_id=self.request.user.id, category=category)
        return super().perform_create(serializer)

    @action(detail=False, methods=['POST'], parser_classes=[CSVParser])
    def upload(self, request):
        serializer = ContactsSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ContactsCategoryViewset(viewsets.ModelViewSet):
    queryset = ContactsCategory.objects.all()
    serializer_class = ContactsCategorySerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super(ContactsCategoryViewset, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)