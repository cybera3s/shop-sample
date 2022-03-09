from django.urls import path

from accounts.views import *
app_name = 'accounts'

urlpatterns = [
    path('regitser/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('verify/', UserRegisterVerifyCodeView.as_view(), name='verify_code')
]