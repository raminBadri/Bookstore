from rest_framework import serializers
from .models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['about', 'creation_date', 'is_deleted', 'is_active', 'modification_date']
