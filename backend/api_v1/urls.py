from django.urls import path, include
from .viewsets.numbers import (
    NumbersViewset,
    DetailNumbersViewset,
    NumberSettingsViewset,
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
    WhastappMediaDetailViewset,
    FriendMessagesViewset
)
from .viewsets.contacts import ContactsViewset
from .viewsets.media import UsersMediaViewset
from .viewsets.settings import SettingViewset
from .viewsets.users import UsersViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('media', UsersMediaViewset, base_name='api_media')
router.register('contacts', ContactsViewset, base_name='api_contacts')
router.register('users', UsersViewset, base_name='api_users')
router.register('friend-messages', FriendMessagesViewset, base_name='api_friend_message')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('users_auth.urls')),
    path('setting/', SettingViewset.as_view(), name='api_setting' ),
    path('numbers/', NumbersViewset.as_view(), name='api_numbers'),
    path('numbers/<int:pk>/', DetailNumbersViewset.as_view(), name='api_number_detail'),
    path('numbers/<int:pk>/start/', StartNumber.as_view(), name='api_number_start'),
    path('numbers/<int:pk>/stop/', StopNumber.as_view(), name='api_number_stop'),
    path('numbers/<int:pk>/status/', StatusNumber.as_view(), name='api_number_status'),
    path('numbers/<int:pk>/setting/', NumberSettingsViewset.as_view(), name='api_number_setting'),
    path('numbers/<int:pk>/login/', LoginNumber.as_view(), name='api_number_login'),
    # path('numbers/<int:pk>/logout/'),
    path('numbers/<int:pk>/chats/', WhatsappChatViewset.as_view(), name='api_messages_chat'),
    path('numbers/<int:pk>/chats/<int:id>/', WhatsappChatDetailViewset.as_view(), name='api_messages_chat_detail'),
    path('numbers/<int:pk>/media/', WhatsappMediaViewset.as_view(), name='api_messages_media'),
    path('numbers/<int:pk>/media/<int:id>/', WhastappMediaDetailViewset.as_view(), name='api_messages_media_detail'),
    path('messages/', WhatsappChatAllViewset.as_view(), name='api_messages_all')
]