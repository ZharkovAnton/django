from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class UserGender(IntegerChoices):
    UNKNOWN = (0, _('Unknown'))
    MAN = (1, _('Man'))
    FEMALE = (2, _('Female'))
