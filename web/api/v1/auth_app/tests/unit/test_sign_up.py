import pytest
from django.urls import reverse

from conftest import locmem_email_backend

pytestmark = [pytest.mark.django_db]


@locmem_email_backend
@pytest.mark.parametrize(
    ['test_input', 'test_output', 'status_code'],
    [
        (
            {
                'first_name': 'test',
                'last_name': 'test',
                'email': 'test@example.com',
                'password_1': 'rttrrt1555',
                'password_2': 'rttrrt1555',
            },
            {'detail': 'Confirmation email has been sent'},
            201,
        ),
        (
            {
                'first_name': 'test',
                'last_name': 'test',
                'email': 'test@example',
                'password_1': 'rttrrt1555',
                'password_2': 'rttrrt1555',
            },
            {'email': ['Enter a valid email address.']},
            400,
        ),
        (
            {
                'last_name': 'test',
                'email': 'test@example.com',
                'password_1': 'rttrrt1555',
                'password_2': 'rttrrt1555',
            },
            {'first_name': ['This field is required.']},
            400,
        ),
        (
            {
                'first_name': 'test',
                'email': 'test@example.com',
                'password_1': 'rttrrt1555',
                'password_2': 'rttrrt1555',
            },
            {'last_name': ['This field is required.']},
            400,
        ),
        (
            {
                'first_name': 'test',
                'last_name': 'test',
                'password_1': 'rttrrt1555',
                'password_2': 'rttrrt1555',
            },
            {'email': ['This field is required.']},
            400,
        ),
        (
            {
                'first_name': 'test',
                'last_name': 'test',
                'email': 'test@example.com',
                'password_2': 'rttrrt1555',
            },
            {'password_1': ['This field is required.']},
            400,
        ),
        (
            {
                'first_name': 'test',
                'last_name': 'test',
                'email': 'test@example.com',
                'password_1': 'rttrrt1555',
            },
            {'password_2': ['This field is required.']},
            400,
        ),
        (
            {
                'first_name': 'test',
                'last_name': 'test',
                'email': 'test@example.com',
                'password_1': 'rtt',
                'password_2': 'rtt',
            },
            {
                'password_1': ['Ensure this field has at least 8 characters.'],
                'password_2': ['Ensure this field has at least 8 characters.'],
            },
            400,
        ),
        (
            {
                'first_name': 'test',
                'last_name': 'test',
                'email': 'test@example.com',
                'password_1': 'rttrrt1555',
                'password_2': 'rttrrt1554',
            },
            {'password_2': ['The two password fields did not match']},
            400,
        ),
    ],
)
def test_sign_up_validation(client, test_input, test_output, status_code):
    url = reverse('api:v1:auth_app:sign-up')
    response = client.post(url, data=test_input)
    assert response.status_code == status_code
    assert response.json() == test_output
