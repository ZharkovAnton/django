from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import Client
import pytest

from api.v1.auth_app.services import AuthAppService

User = get_user_model()

pytestmark = [pytest.mark.django_db]

@pytest.fixture
def auth_service():
    return AuthAppService()

@pytest.fixture
def user() -> User:
    return User.objects.create_user(email='q@gmail.com', password='12345678', is_active=True)

@pytest.fixture
def user_token(user)-> tuple[str, str]:
    refresh = RefreshToken().for_user(user)
    return str(refresh), refresh.access_token

@pytest.fixture
def api_client(client, user_token) -> Client:
    # client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {user_token}'
    client.cookies['jwt-auth'] = user_token[1]
    client.cookies['refresh'] = user_token[0]
    return client
