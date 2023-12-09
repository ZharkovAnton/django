import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


def test_current_profile(api_client, user):
    url = reverse('api:v1:profile_app:profile', kwargs={'user_id': user.id})
    response = api_client.get(url)
    assert response.status_code == 200

    expected_data = {
        'id': 1,
        'first_name': user.first_name,
        'full_name': user.full_name,
        'last_name': user.last_name,
        'email': user.email,
        'birthday': user.birthday,
        'gender': user.gender,
        'avatar': user.avatar.url,
        'count_articles': 0,
        'count_comments': 0,
        'total_likes': 0,
        'count_followers': 0,
        'followers': [],
    }
    assert response.json() == expected_data


def test_unauthorized_access(client, user):
    url = reverse('api:v1:profile_app:profile', kwargs={'user_id': user.id})
    response = client.get(url)
    assert response.status_code == 200


def test_update_avatar_auth(api_client, user, image_content_file):
    assert user.avatar.size != image_content_file.size
    url = reverse('api:v1:profile_app:profile-avatar-update')
    data = {'avatar': image_content_file}
    response = api_client.post(url, data)
    assert response.status_code == 200
    user.refresh_from_db()

    assert user.avatar.size == image_content_file.size


def test_auth_user_update_his_profile_info(api_client, user):
    url = reverse('api:v1:profile_app:profile-bio-update')
    data = {'first_name': 'Ivan', 'last_name': 'Ivanov', 'birthday': '2023-11-14', 'gender': 0}
    response = api_client.post(url, data=data)
    assert response.status_code == 200

    user.refresh_from_db()
    assert user.first_name == data['first_name']
    assert user.last_name == data['last_name']
    assert user.birthday.strftime('%Y-%m-%d') == data['birthday']
    assert user.gender == data['gender']


def test_auth_user_update__profile_info(client):
    url = reverse('api:v1:profile_app:profile-bio-update')
    data = {'first_name': 'Ivan', 'last_name': 'Ivanov', 'birthday': '2023-11-14', 'gender': 0}
    response = client.post(url, data=data)
    assert response.status_code == 401
