from django.core.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentications.serializers import (
    LoginSerializer,
    MerchantLoginSerializer,
    TokenRefreshSerializer,
    UserLoginSerializer,
    UserMeSerializer,
)
from apps.users.models import User
from utils.response.resp import APIResponse


class MerchantLoginAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        req_data = request.data
        login_serializer = LoginSerializer(data=req_data)
        login_serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=req_data["email"])

        if user.is_merchant is False:
            raise PermissionDenied

        user_serializer = MerchantLoginSerializer(user)
        data = {
            "user": user_serializer.data,
            "token": login_serializer.validated_data,
        }
        return Response(
            APIResponse.get_response(
                data=data,
            )
        )


class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        req_data = request.data
        login_serializer = LoginSerializer(data=req_data)
        login_serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=req_data["email"])

        if user.is_merchant is True:
            raise PermissionDenied

        user_serializer = UserLoginSerializer(user)
        data = {
            "user": user_serializer.data,
            "token": login_serializer.validated_data,
        }
        return Response(
            APIResponse.get_response(
                data=data,
            )
        )


class RefreshTokenAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=TokenRefreshSerializer)
    def post(self, request):
        req_data = request.data
        serializer = TokenRefreshSerializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        data = {
            "token": serializer.validated_data,
        }
        return Response(
            APIResponse.get_response(
                data=data,
            )
        )


class UserMeAPIView(APIView):
    @swagger_auto_schema(tags=["User"])
    def get(self, request):
        user = request.user

        user_serializer = UserMeSerializer(user)
        data = {
            "user": user_serializer.data,
        }
        return Response(
            APIResponse.get_response(
                data=data,
            )
        )
