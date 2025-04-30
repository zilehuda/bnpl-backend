from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer as SimpleJWTTokenRefreshSerializer,
)

from apps.users.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "is_merchant",
        )


class MerchantLoginSerializer(BaseUserSerializer):
    pass


class UserLoginSerializer(BaseUserSerializer):
    pass


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class TokenRefreshSerializer(SimpleJWTTokenRefreshSerializer):
    refresh = serializers.CharField(required=True)


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
            "is_merchant",
        )
