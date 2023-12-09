import urllib
from typing import TYPE_CHECKING, NamedTuple, Optional
from urllib.parse import urlencode, urljoin

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from api.email_services import BaseEmailHandler

from main.decorators import except_shell

if TYPE_CHECKING:
    from main.models import UserType

User: 'UserType' = get_user_model()


class CreateUserData(NamedTuple):
    first_name: str
    last_name: str
    email: str
    password_1: str
    password_2: str


class ConfirmationEmailHandler(BaseEmailHandler):
    FRONTEND_URL = settings.FRONTEND_URL
    FRONTEND_PATH = 'verify-email/'
    TEMPLATE_NAME = 'email/auth_app/confirm_email.html'

    def _get_activate_url(self) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        query_params: str = urlencode(
            {
                'key': self.user.confirmation_key,
            },
            safe=':+',
        )
        return f'{url}?{query_params}'

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('Register confirmation email'),
            'to_email': self.user.email,
            'context': {
                'user': self.user.full_name,
                'activate_url': self._get_activate_url(),
            },
        }


class AuthAppService:
    @staticmethod
    def is_user_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str) -> User:
        return User.objects.get(email=email)

    @transaction.atomic()
    def create_user(self, validated_data: dict):
        data = CreateUserData(**validated_data)
        user = User.objects.create_user(
            email=data.email,
            password=data.password_1,
            first_name=data.first_name,
            last_name=data.last_name,
            is_active=False,
        )
        return user


def full_logout(request):
    response = Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)
    auth_cookie_name = settings.REST_AUTH['JWT_AUTH_COOKIE']
    refresh_cookie_name = settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE']

    response.delete_cookie(auth_cookie_name)
    refresh_token = request.COOKIES.get(refresh_cookie_name)
    if refresh_cookie_name:
        response.delete_cookie(refresh_cookie_name)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except KeyError:
        response.data = {"detail": _("Refresh token was not included in request data.")}
        response.status_code = status.HTTP_401_UNAUTHORIZED
    except (TokenError, AttributeError, TypeError) as error:
        if hasattr(error, 'args'):
            if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                response.data = {"detail": _(error.args[0])}
                response.status_code = status.HTTP_401_UNAUTHORIZED
            else:
                response.data = {"detail": _("An error has occurred.")}
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        else:
            response.data = {"detail": _("An error has occurred.")}
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        message = _(
            "Neither cookies or blacklist are enabled, so the token "
            "has not been deleted server side. Please make sure the token is deleted client side."
        )
        response.data = {"detail": message}
        response.status_code = status.HTTP_200_OK
    return response


class ResetPasswordEmail(BaseEmailHandler):
    FRONTEND_URL = settings.FRONTEND_URL
    FRONTEND_PATH = 'password-change/'
    TEMPLATE_NAME = 'email/auth_app/reset_password_email.html'

    def _get_activate_url(self) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        token, uid = PasswordResetHandler().user_token_uid(self.user.email)

        query_params: str = urlencode(
            {'uid': uid, 'token': token},
            safe=':+',
        )
        return f'{url}?{query_params}'

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('Reset password email'),
            'to_email': self.user.email,
            'context': {
                'activate_url': self._get_activate_url(),
            },
        }


class PasswordResetHandler:
    @staticmethod
    def get_user(email: str) -> Optional[User]:
        try:
            return User.objects.get(email=email)
        except (
            User.DoesNotExist
        ):  # нельзя возвращать ответ что такого email нет, так как могут начать подбирать email,
            # нужно всегда писать что письмо отправлено
            return None

    def user_token_uid(self, email: str):
        user = self.get_user(email)
        if not user:
            return None, None
        token, uid = self.generate_token_uid(user)
        return token, uid

    @staticmethod
    def generate_token_uid(user: User) -> tuple[str, str]:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return token, uid

    @staticmethod
    def check_uid_token(token: str, uid: str) -> User:
        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError('Invalid uid')

        if not default_token_generator.check_token(user, token):
            raise ValidationError('Invalid token')

        return user


class CaptchaHandler:
    def __init__(self, token: str):
        self.token = token

    def _get_captcha_response(self) -> dict or None:
        url = 'https://www.google.com/recaptcha/api/siteverify'
        params = urlencode({'secret': settings.DRF_RECAPTCHA_SECRET_KEY, 'response': self.token})
        data = f'{url}?{params}'
        try:
            req = urllib.request.Request(data, method='POST')
            response = urllib.request.urlopen(req)
            return json.loads(response.read().decode())
        except urllib.error.HTTPError:
            return None

    def check_captcha_response(self) -> bool:
        response = self._get_captcha_response()
        if response and response['score'] >= 0.7:
            return True

        return False


class MicroAuthHandler:
    def __init__(self, data: dict):
        self.token = data['token']

    def verify_jwt_token(self) -> int:
        access_token = AccessToken(self.token)
        return access_token.payload['user_id']

    def get_user(self) -> User | None:
        user_id = self.verify_jwt_token()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise User.DoesNotExist('User does not exist')


class CheckChatUserHandler:
    def check_chat_user(self, id: int) -> int | None:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None
