from typing import TypeVar

from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import UserGender
from .managers import UserManager
from .services import user_directory_path

UserType = TypeVar('UserType', bound='User')


class User(AbstractUser):
    username = None  # type: ignore
    email = models.EmailField(_('Email address'), unique=True)
    birthday = models.DateField(_('Birthday'), null=True, blank=True)
    gender = models.PositiveSmallIntegerField(_('Gender'), choices=UserGender.choices, default=UserGender.UNKNOWN)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, default='no-image-available.jpg')
    following = models.ManyToManyField(
        'self',
        blank=True,
        related_name='followers',
        symmetrical=False,
        through='actions.Follower',
    )

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()  # type: ignore

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        return super().get_full_name()

    @property
    def confirmation_key(self) -> str:
        return signing.dumps(obj=self.pk)
