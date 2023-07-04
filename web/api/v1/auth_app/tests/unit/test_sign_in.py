from django.urls import reverse
import pytest

pytestmark = [pytest.mark.django_db]

@pytest.mark.parametrize(
        ['test_input', 'status_code', 'is_access'],
        [
            ({'email': 'q@gmail.com' ,'password': '12345678'}, 200, True),
            ({'email': 'q2@gmail.com' ,'password': '1234678'}, 400, False),
            ({'email': 'q@gmail.com' ,'password': '34678'}, 400, False),
            ({'password': '1234678'}, 400, False),
            ({'email': 'q@gmail.com'}, 400, False)
        ])
def test_success_sign_in(client, user, test_input, status_code, is_access):
    url = reverse('api:v1:auth_app:sign-in')

    response = client.post(url, data=test_input, format='json')
    assert response.status_code == status_code

    data = response.json()
    assert bool(data.get('access')) == is_access
