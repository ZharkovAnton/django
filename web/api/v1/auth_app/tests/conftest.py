from django.contrib.auth import get_user_model
import pytest

User = get_user_model()

pytestmark = [pytest.mark.django_db]

@pytest.fixture
def user() -> User:
    return User.objects.create_user(email='q@gmail.com', password='12345678')
