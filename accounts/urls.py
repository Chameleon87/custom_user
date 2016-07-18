from django.conf.urls import url, include
from rest_framework.authtoken import views
from views import RegisterView, Login

urlpatterns = [
    url(r'^auth/register/?$', RegisterView.as_view(), name='register'),
    url(r'^auth/login', Login)
]
