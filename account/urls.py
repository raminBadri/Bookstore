from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    # this url path is for generate authentication token.
    # client can now request to address below to take his/her auth token in API view.
    # requests must be POST and Multipart Form, parameters to send: username & password
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    ]
