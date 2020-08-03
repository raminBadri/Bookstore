from django.contrib.auth.forms import UserCreationForm
from account.models import ShopUser
from django import forms


class SignupFrom(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required', label='email')

    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'gender', 'password1', 'password2')
