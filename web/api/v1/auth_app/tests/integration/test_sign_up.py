from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail

from api.v1.auth_app.tests.conftest import locmem_email_backend

import re

import pytest

pytestmark = [pytest.mark.django_db]

User = get_user_model()

@locmem_email_backend
def test_sent_email_and_confirm(client):
    # Testing sending an email
    url = reverse('api:v1:auth_app:sign-up')
    data = {
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@example.com',
        'password_1': 'rttrrt1555',
        'password_2': 'rttrrt1555',
    }
    response = client.post(url, data=data)
    assert response.status_code == 201
    assert len(mail.outbox) == 1
    user = User.objects.get(email=data['email'])
    assert not user.is_active

    # Verification link testing
    email_message = mail.outbox[0]
    key = re.search(r'key=?([^\">]+)', str(email_message.message()))[1]
    data_verify = {
        'key': key
    }
    verify_url = reverse('api:v1:auth_app:sign-up-verify')
    verify_response = client.post(verify_url, data=data_verify)
    assert verify_response.status_code == 200
    assert verify_response.json() == {'detail': 'Email verified'}
    user.refresh_from_db()
    assert user.is_active
