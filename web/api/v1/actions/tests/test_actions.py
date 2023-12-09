import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


def test_update_avatar_unauth(client, user, image_content_file):
    url = reverse('api:v1:profile_app:profile-avatar-update')
    data = {'avatar': image_content_file}
    response = client.post(url, data)
    assert response.status_code == 401


def test_follow_unfollow_update(api_client, user, second_user):
    url = reverse('api:v1:actions:followers-update')
    data = {
        'id': second_user.id,
    }
    response = api_client.post(url, data=data)
    assert response.status_code == 200

    assert user.following.count() == 1
    assert user.following.all().first().id == second_user.id
    assert second_user.followers.count() == 1
    assert second_user.followers.all().first().id == user.id

    response = api_client.post(url, data=data)
    assert response.status_code == 200

    assert user.following.count() == 0
    assert second_user.followers.count() == 0


def test_get_following_current_user(api_client, user_with_following_followers, second_user):
    url = reverse('api:v1:actions:following-current-user')
    response = api_client.get(url)
    assert response.status_code == 200

    response_data = response.json()
    assert all(key in response_data for key in ['count', 'next', 'previous', 'results'])

    expected_data = {
        'id': second_user.id,
        'full_name': second_user.full_name,
        'avatar': second_user.avatar.url,
        'email': second_user.email,
        'followers': [user_with_following_followers.id],
    }
    assert response_data['results'][0] == expected_data


def test_get_followers_current_user(api_client, user_with_following_followers, second_user):
    url = reverse('api:v1:actions:followers-current-user')
    response = api_client.get(url)
    assert response.status_code == 200

    response_data = response.json()
    assert all(key in response_data for key in ['count', 'next', 'previous', 'results'])

    expected_data = {
        'id': second_user.id,
        'full_name': second_user.full_name,
        'avatar': second_user.avatar.url,
        'email': second_user.email,
        'followers': [user_with_following_followers.id],
    }
    assert response_data['results'][0] == expected_data


def test_get_following_other_user(api_client, user_with_following_followers, second_user):
    url = reverse('api:v1:actions:following-by-id', kwargs={'user_id': second_user.id})
    response = api_client.get(url)
    assert response.status_code == 200

    response_data = response.json()
    assert all(key in response_data for key in ['count', 'next', 'previous', 'results'])

    expected_data = {
        'id': user_with_following_followers.id,
        'full_name': user_with_following_followers.full_name,
        'avatar': user_with_following_followers.avatar.url,
        'email': user_with_following_followers.email,
        'followers': [second_user.id],
    }
    assert response_data['results'][0] == expected_data


def test_get_followers_other_user(api_client, user_with_following_followers, second_user):
    url = reverse('api:v1:actions:followers-by-id', kwargs={'user_id': second_user.id})
    response = api_client.get(url)
    assert response.status_code == 200

    response_data = response.json()
    assert all(key in response_data for key in ['count', 'next', 'previous', 'results'])

    expected_data = {
        'id': user_with_following_followers.id,
        'full_name': user_with_following_followers.full_name,
        'avatar': user_with_following_followers.avatar.url,
        'email': user_with_following_followers.email,
        'followers': [second_user.id],
    }
    assert response_data['results'][0] == expected_data
