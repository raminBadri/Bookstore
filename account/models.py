from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UnicodeUsernameValidator


class ShopUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    gender_types = [('m', 'male'), ('f', 'female')]
    gender = models.CharField(max_length=1, choices=gender_types, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
