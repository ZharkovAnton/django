from django.contrib.auth import get_user_model

import pytest

pytestmark = [pytest.mark.django_db]

User = get_user_model()

class TestAuthService:
    def test_is_user_exists(self, user, auth_service):
        assert not auth_service.is_user_exist('test_false@gmail.com')
        assert auth_service.is_user_exist(user.email)

    def test_get_user(self, user, auth_service):
        assert auth_service.get_user(user.email)
        assert not auth_service.get_user('test_false@gmail.com')


    def test_create_user(self, auth_service):
        data = {
            'email': 'test@gmail.com',
            'first_name': 'test',
            'last_name': 'test2',
            'password_1': 'test1234',
            'password_2': 'test1234',
            }
        user = auth_service.create_user(data)
        assert isinstance(user, User)
        assert user.email == data['email']
        assert user.first_name == data['first_name']
        assert user.last_name == data['last_name']
        assert user.check_password(data['password_1'])
