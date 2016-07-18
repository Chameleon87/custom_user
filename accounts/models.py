from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.

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
