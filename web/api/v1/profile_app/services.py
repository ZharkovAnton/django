from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ProfileUpdateService:
    def update_user(self, user: User, data: dict) -> User:
        updated_fields = []
        for attr, value in data.items():
            if getattr(user, attr) != value:
                setattr(user, attr, value)
                updated_fields.append(attr)
        user.save(update_fields=updated_fields)

    def update_password(self, user: User, data: dict):
        user.set_password(data['password_1'])
        user.save(update_fields=['password'])

    def update_avatar(self, user: User, avatar: InMemoryUploadedFile):
        user.avatar = avatar
        user.save(update_fields=['avatar'])
