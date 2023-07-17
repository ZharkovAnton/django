from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response

User = get_user_model()

class ProfileUpdateService:
    def update_user(self, user: User, data: dict) -> User:
        for attr, value in data.items():
            setattr(user, attr, value)
        user.save()

    def update_password(self, user: User, data: dict):
        user.set_password(data['password_1'])
        user.save(update_fields=['password'])
    # Todo: add InMemoryUploadedFile typing
    def update_avatar(self, user: User, avatar):
        user.avatar = avatar
        user.save(update_fields=['avatar'])
