from django.conf.urls import url, include
from rest_framework.authtoken import views
from views import RegisterView, obtain_auth_token

urlpatterns = [
    url(r'^auth/register/?$', RegisterView.as_view(), name='register'),
    url(r'^auth/login', obtain_auth_token, name='login')
]
