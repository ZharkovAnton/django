from django.urls import reverse

import pytest

pytestmark = [pytest.mark.django_db]

def test_logout(api_client):
    url = reverse('api:v1:auth_app:logout')
    assert api_client.cookies.get('jwt-auth').value
    assert api_client.cookies.get('refresh').value
    
    response = api_client.post(url)
    assert response.status_code == 200
    assert not api_client.cookies.get('jwt-auth').value
    assert not api_client.cookies.get('refresh').value
