from typing import TYPE_CHECKING

from dj_rest_auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.core import signing
from django.core.signing import BadSignature
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers
from .services import (
    AuthAppService,
    CaptchaHandler,
    ConfirmationEmailHandler,
    MicroAuthHandler,
    PasswordResetHandler,
    ResetPasswordEmail,
    full_logout,
)

if TYPE_CHECKING:
    from main.models import UserType

User: 'UserType' = get_user_model()


class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AuthAppService()
        user = service.create_user(serializer.validated_data)

        email = ConfirmationEmailHandler(user)
        email.send_email()

        return Response(
            {'detail': _('Confirmation email has been sent')},
            status=status.HTTP_201_CREATED,
        )


class LoginView(auth_views.LoginView):
    # TODO: убрать класс auth_views.LoginView и переписать
    serializer_class = serializers.LoginSerializer


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = PasswordResetHandler().get_user(serializer.validated_data['email'])
        if user:
            email = ResetPasswordEmail(user)
            email.send_email()

        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        handler = PasswordResetHandler()

        user = handler.check_uid_token(
            token=serializer.validated_data['token'],
            uid=serializer.validated_data['uid'],
        )

        user.set_password(serializer.validated_data['password_1'])
        user.save(update_fields=["password"])
        return Response(
            {'detail': _('Password has been reset with the new password.')},
            status=status.HTTP_200_OK,
        )


class VerifyEmailView(GenericAPIView):
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_id = signing.loads(serializer.validated_data["key"])
            user = User.objects.get(id=user_id)
        except (TypeError, ValueError, User.DoesNotExist, BadSignature):
            user = None

        if user:
            user.is_active = True
            user.save()
            return Response(
                {'detail': _('Email verified')},
                status=status.HTTP_200_OK,
            )

        return Response(
            {'detail': _('Email not verified')},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CaptchaView(GenericAPIView):
    serializer_class = serializers.CaptchaSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        captcha = CaptchaHandler(serializer.validated_data['token'])

        if captcha.check_captcha_response():
            return Response(
                {'detail': _('success')},
                status=status.HTTP_200_OK,
            )

        return Response(
            {'detail': _('bad')},
            status=status.HTTP_400_BAD_REQUEST,
        )


class MicroAuthView(GenericAPIView):
    serializer_class = serializers.MicroAuthSerializer
    # TODO: ??? здесь как я понимаю не нужно ставить доступ для авторизованныз пользователей
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = MicroAuthHandler(serializer.validated_data)
        user = service.get_user()

        user_serializer = serializers.UserSerializer(user)

        return Response(user_serializer.data)
