from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
app_name = 'users_auth'
urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]