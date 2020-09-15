from django.contrib.auth.forms import UserCreationForm
from account.models import ShopUser
from django import forms


class SignupFrom(UserCreationForm):
    email = forms.EmailField(max_length=200, label='Email', widget=forms.EmailInput(attrs=
                                                                                    {'placeholder': 'required'}))

    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'gender', 'password1', 'password2')
