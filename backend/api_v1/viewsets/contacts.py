from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from ..serializers.contacts import GroupContactsSerializer, ContactsSerializer, ValidateContactsSerializer
from contacts_app.models import Contacts, GroupContacts
from users_auth.permissions import HasAPIAccess, HasWhatsappLoggedIn
from driver_manager.drivers import status_number
from numbers_app.models import WhatsappNumbers
from driver_manager.notifier import HandleValidateNumber

class ContactsViewset(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super(ContactsViewset, self).get_queryset()
        queryset = queryset.filter(group__user_id=self.request.user.id)
        return queryset


class GroupContactsViewset(viewsets.ModelViewSet):
    queryset = GroupContacts.objects.all()
    serializer_class = GroupContactsSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super(GroupContactsViewset, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

# class GroupContactsViewset(viewsets.ModelViewSet):
#     queryset = GroupContacts.objects.all()
#     serializer_class = GroupContactsSerializer
#     authentication_classes = (TokenAuthentication, )
#     permission_classes = (IsAuthenticated, )
#     lookup_url_kwarg = 'group_id'

#     def get_queryset(self):
#         queryset = super(GroupContactsViewset, self).get_queryset()
#         queryset = queryset.filter(user_id=self.request.user.id)
#         return queryset

#     def perform_create(self, serializer):
#         serializer.save(user_id=self.request.user.id)

#     @action(detail=True, methods=['POST'])
#     def validate(self, request, group_id=None):
#         group = self.get_object()
#         contacts = group.contacts.filter(is_active=False)
#         serializer = ValidateContactsSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         id = serializer.data.get('number_id')
#         number = WhatsappNumbers.objects.filter(user_id=group.user.id, id=id)
#         if not number.exists():
#             return Response({"detail":"number_id not found"}, status=404)
#         HandleValidateNumber(id, contacts).start()
#         return Response({"detail":"validate contacts started"}, status=102)

#     @action(detail=True, methods=['GET', 'POST', 'DELETE'])
#     def contacts(self, request, group_id=None, contact_id=None):
#         group = self.get_object()
#         contact_list = group.contacts
        
#         if request.method == 'GET':
#             serializer = ContactsSerializer(contact_list, many=True)
#             return Response(serializer.data)
#         elif request.method == 'POST':
#             serializer = ContactsSerializer(data=request.data, many=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save(group_id=group.id)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=201, headers=headers)
#         elif request.method == 'DELETE':
#             contact_list.delete()
#             return Response(status=204)

#     def contact_detail(self, request, group_id=None, contact_id=None):
#         group = self.get_object()
#         contact = group.contacts.get(id=contact_id)

#         if request.method == 'GET':
#             serializer = ContactsSerializer(contact)
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#             serializer = ContactsSerializer(contact, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)
#         elif request.method == 'DELETE':
#             contact.delete()
#             return Response(status=204)