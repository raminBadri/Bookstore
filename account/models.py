from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    gender_types = [('m', 'male'), ('f', 'female')]
    gender = models.CharField(max_length=1, choices=gender_types, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.IntegerField(null=True, blank=True)
