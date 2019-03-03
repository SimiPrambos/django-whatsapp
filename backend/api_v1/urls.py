from django.urls import path, include
from .viewsets.numbers import (
    NumbersViewset,
    DetailNumbersViewset,
    StartNumber,
    StopNumber,
    StatusNumber,
    LoginNumber,
)
from .viewsets.messages import (
    WhatsappChatAllViewset,
    WhatsappChatViewset,
    WhatsappChatDetailViewset,
    WhatsappMediaViewset,
    WhastappMediaDetailViewset
)
from .viewsets.contacts import ContactsViewset, GroupContactsViewset
from .viewsets.media import UsersMediaViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('media', UsersMediaViewset, base_name='api_media')
router.register('group', GroupContactsViewset, base_name='api_group')
router.register('contacts', ContactsViewset, base_name='api_contacts')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('users_auth.urls')),
    # path('group/<int:group_id>/contacts/<int:contact_id>/', GroupContactsViewset.as_view(
    #     {"get":"contact_detail", "put":"contact_detail", "delete":"contact_detail"})),
    # path('contacts/', ContactsViewset.as_view(), name='api_contacts'),
    path('numbers/', NumbersViewset.as_view(), name='api_numbers'),
    path('numbers/<int:pk>/', DetailNumbersViewset.as_view(), name='api_number_detail'),
    path('numbers/<int:pk>/start/', StartNumber.as_view(), name='api_number_start'),
    path('numbers/<int:pk>/stop/', StopNumber.as_view(), name='api_number_stop'),
    path('numbers/<int:pk>/status/', StatusNumber.as_view(), name='api_number_status'),
    path('numbers/<int:pk>/login/', LoginNumber.as_view(), name='api_number_login'),
    # path('numbers/<int:pk>/logout/'),
    path('numbers/<int:pk>/chats/', WhatsappChatViewset.as_view(), name='api_messages_chat'),
    path('numbers/<int:pk>/chats/<int:id>/', WhatsappChatDetailViewset.as_view(), name='api_messages_chat_detail'),
    path('numbers/<int:pk>/media/', WhatsappMediaViewset.as_view(), name='api_messages_media'),
    path('numbers/<int:pk>/media/<int:id>/', WhastappMediaDetailViewset.as_view(), name='api_messages_media_detail'),
    path('messages/', WhatsappChatAllViewset.as_view(), name='api_messages_all')
]