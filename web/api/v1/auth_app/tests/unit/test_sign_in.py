from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest

pytestmark = [pytest.mark.django_db]

def test_success_sign_in(client, user):
    url = reverse('api:v1:auth_app:sign-in')
    data = {
        'email': user.email,
        'password': '12345678'
    }
    response = client.post(url, data=data, format='json')
    assert response.status_code == 200
    data = response.json()
    assert data['access']
