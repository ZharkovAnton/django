from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail

from api.v1.auth_app.tests.conftest import locmem_email_backend

import re

import pytest

pytestmark = [pytest.mark.django_db]

User = get_user_model()

@locmem_email_backend
def test_reset_password(client, user):
    # Test sending an email with a link to change the password
    url = reverse('api:v1:auth_app:reset-password')
    data = {
        'email': user.email,
    }
    reset_password_response = client.post(url, data, format='json')
    assert reset_password_response.status_code == 200
    assert len(mail.outbox) == 1

    # Password change test
    email_message = mail.outbox[0]
    link_change_password = re.search(r'href=[\"]?([^\">]+)', str(email_message.message()))[1]
    assert link_change_password
    print(f'THIS IS LINK:{link_change_password}') # почему & кодируется как &amp; в ссылке http://localhost:8000/password-change/?uid=MQ&amp;token=bqib6g-a771a6fa5166f77ffddef413e89cfdc3
    uid = re.search(r'uid=?([^\&>]+)', link_change_password)[1]
    token = re.search(r'token=?([^\;>]+)', link_change_password)[1]
    assert uid
    assert token
    data_confirm = {
        'password_1':'nmlK345k',
        'password_2':'nmlK345k',
        'token': token,
        'uid': uid,
    }
    url_change_password = reverse('api:v1:auth_app:reset-password-confirm')
    reset_password_confirm_response = client.post(url_change_password, data=data_confirm, format='json')
    assert reset_password_confirm_response.status_code == 200

    # Test login with new password
    url = reverse('api:v1:auth_app:sign-in')
    data_login = {
        'email': user.email,
        'password': data_confirm['password_1']
    }
    response = client.post(url, data=data_login, format='json')
    assert response.status_code == 200
    data = response.json()
    assert data['access']

def test_client(api_client):
    url = reverse('api:v1:blog:article-list')
    response = api_client.get(url)
    print(f'Code: {response.status_code}')


