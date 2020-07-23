from rest_framework import serializers
from .models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['about', 'creation_date', 'is_deleted', 'is_active', 'modification_date']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ['bio', 'creation_date', 'is_deleted', 'is_active', 'modification_date']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'
