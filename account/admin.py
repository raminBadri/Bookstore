from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShopUser

admin.site.register(ShopUser, UserAdmin)
