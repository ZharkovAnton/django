from django.urls import reverse
from django.core import mail
from django.test.utils import override_settings

import pytest

pytestmark = [pytest.mark.django_db]


locmem_email_backend = override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CELERY_TASK_ALWAYS_EAGER=True,
)

@locmem_email_backend
@pytest.mark.parametrize(
    ['test_input', 'test_output', 'status_code', 'is_sent_mail'],
    [
        ({'email': 'q@gmail.com'}, {'detail': 'Password reset e-mail has been sent.'}, 200, True),
        ({'email': 'q123@gmail.com'}, {'detail': 'Password reset e-mail has been sent.'}, 200, False),
    ])
def test_reset_password(client, user, test_input, test_output, status_code, is_sent_mail):
    url = reverse('api:v1:auth_app:reset-password')
    response = client.post(url, test_input)
    print(response.json())
    assert response.status_code == status_code
    assert response.json() == test_output
    assert len(mail.outbox) == is_sent_mail
