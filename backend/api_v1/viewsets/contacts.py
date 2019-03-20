import unicodecsv as csv
import codecs
import io
import six
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from ..serializers.contacts import ContactsSerializer
from contacts_app.models import Contacts
from users_auth.permissions import HasAPIAccess, HasWhatsappLoggedIn
from driver_manager.drivers import status_number
from numbers_app.models import WhatsappNumbers
from rest_framework.parsers import MultiPartParser, FileUploadParser

class ContactsViewset(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = super(ContactsViewset, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id).order_by('-created')
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=self.user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @action(detail=False, methods=['POST'], parser_classes=[MultiPartParser])
    def upload(self, request):
        file = request.FILES.get('file')
        if file and not file.name.rsplit('.')[-1] == 'csv':
            return Response({"detail":"File type is not allowed. make sure your file is csv format."}, status=400)
        data = None
        try:
            binary = universal_newlines(file.read())
            rows = unicode_csv_reader(binary, delimiter=',', charset='utf-8')
            data = OrderedRows(next(rows))
            for row in rows:
                row_data = dict(zip(data.header, row))
                data.append(row_data)
        except:
            pass
        print(data)
        serializer = ContactsSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


def universal_newlines(stream):
    for line in stream.splitlines():
        yield line

def unicode_csv_reader(csv_data, dialect=csv.excel, charset='utf-8', **kwargs):
    csv_reader = csv.reader(csv_data, dialect=dialect, encoding=charset, **kwargs)
    for row in csv_reader:
        yield row


class OrderedRows(list):
    def __init__(self, header):
        self.header = [c.strip() for c in header] if (header is not None) else None