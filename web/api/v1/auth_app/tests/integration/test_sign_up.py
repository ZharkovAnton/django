from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from django.test.utils import override_settings

import re

import pytest

pytestmark = [pytest.mark.django_db]

User = get_user_model()

locmem_email_backend = override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CELERY_TASK_ALWAYS_EAGER=True,
)

@locmem_email_backend
@pytest.mark.parametrize(
        ['test_input', 'test_output', 'status_code'],
        [
            ({'first_name': 'test', 'last_name': 'test', 'email': 'test@example.com', 'password_1': 'rttrrt1555', 'password_2': 'rttrrt1555',}, {'detail': 'Confirmation email has been sent'}, 201),
            ({'first_name': 'test', 'last_name': 'test', 'email': 'test@example', 'password_1': 'rttrrt1555', 'password_2': 'rttrrt1555',}, {'email': ['Enter a valid email address.']}, 400),
            ({'last_name': 'test', 'email': 'test@example.com', 'password_1': 'rttrrt1555', 'password_2': 'rttrrt1555',}, {'first_name': ['This field is required.']}, 400),
            ({'first_name': 'test', 'email': 'test@example.com', 'password_1': 'rttrrt1555', 'password_2': 'rttrrt1555',}, {'last_name': ['This field is required.']}, 400),
            ({'first_name': 'test', 'last_name': 'test', 'password_1': 'rttrrt1555', 'password_2': 'rttrrt1555',}, {'email': ['This field is required.']}, 400),
            ({'first_name': 'test', 'last_name': 'test', 'email': 'test@example.com', 'password_2': 'rttrrt1555',}, {'password_1': ['This field is required.']}, 400),
            ({'first_name': 'test', 'last_name': 'test', 'email': 'test@example.com', 'password_1': 'rttrrt1555',}, {'password_2': ['This field is required.']}, 400),
            ({'first_name': 'test', 'last_name': 'test', 'email': 'test@example.com', 'password_1': 'rtt', 'password_2': 'rtt',}, {'password_1': ['Ensure this field has at least 8 characters.'],
                                                                                                                                   'password_2': ['Ensure this field has at least 8 characters.']}, 400),
            ({'first_name': 'test', 'last_name': 'test', 'email': 'test@example.com', 'password_1': 'rttrrt1555', 'password_2': 'rttrrt1554',}, {'password_2': ['The two password fields did not match']}, 400)
        ])
def test_sign_up_validation(client, test_input, test_output, status_code):
    url = reverse('api:v1:auth_app:sign-up')
    response = client.post(url, data=test_input)
    assert response.status_code == status_code
    assert response.json() == test_output

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
