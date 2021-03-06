from rest_framework import serializers
from .models import *
from account.models import ShopUser


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    genre = serializers.SlugRelatedField(
        slug_field='title',
        read_only=True,
        many=True
    )

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


"""
In the following API, I used some extra features of DRF rather than above ones.
Firstly, i don't want email field to be write_only and clients can't read this field. 
Secondly, username won't be admin while registering new users via API.
"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        exclude = ('password', 'is_superuser')
        extra_kwargs = {
            'email': {'write_only': True}
        }

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError('username can not be admin')
        return value

    def validate_email(self, value):
        if value is None:
            raise serializers.ValidationError('Email field can not be empty')
        return value
