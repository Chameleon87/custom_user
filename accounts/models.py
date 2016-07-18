from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import UserManager

# Create your models here.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class AcUser(AbstractBaseUser):

    USER_TYPES = (
        ( 'customer', 'Customer'),
        ( 'courier', 'Courier'),
    )

    user_type = models.CharField(max_length=200, choices=USER_TYPES)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['password']
    USERNAME_FIELD = 'email'

    objects = UserManager()
