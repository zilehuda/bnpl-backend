from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from apps.authentications.api.auth_api import (
    MerchantLoginAPIView,
    RefreshTokenAPIView,
    UserLoginAPIView,
    UserMeAPIView,
)

urlpatterns = [
    path("merchants/token/", MerchantLoginAPIView.as_view(), name="merchant_login_api"),
    path("users/token/", UserLoginAPIView.as_view(), name="user_login_api"),
    path("token/refresh/", RefreshTokenAPIView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/me/", UserMeAPIView.as_view(), name="user_me_api"),
]
