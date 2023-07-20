from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from .managers import LikeDislikeManager

User = get_user_model()

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        ('LIKE', 'Like'),
        ('DISLIKE', 'Dislike'),
    )

    vote = models.SmallIntegerField(_('Vote'), choices=VOTES)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    def comments(self):
        return self.get_queryset().filter(content_type__models='comments').order_by(F('created').asc())

    def articles(self):
        return self.get_queryset().filter(content_type__models='articles').order_by(F('created').asc())
