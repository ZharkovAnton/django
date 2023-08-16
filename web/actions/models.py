from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from .managers import LikeDislikeManager

User = get_user_model()


class LikeDislike(models.Model):
    class Vote(models.IntegerChoices):
        LIKE = 1
        DISLIKE = -1

    vote = models.SmallIntegerField(_('Vote'), choices=Vote.choices)
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE, related_name='likes_dislikes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    created = models.DateTimeField(auto_now=True)

    objects = LikeDislikeManager()

    def comments(self):
        return self.get_queryset().filter(content_type__models='comments').order_by(F('created').asc())

    def articles(self):
        return self.get_queryset().filter(content_type__models='articles').order_by(F('created').asc())


class Follower(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('subscriber', 'to_user'), name='follower_subscriber_to_user_unique'),
        )

class EventAction(models.Model):
    class EventChoices(models.TextChoices):
        UPDATE_AVATAR = ('update_avatar', 'Updated avatar')
        CREATE_ARTICLE = ('create_article', 'Created new article')

    name = models.CharField(max_length=255, choices=EventChoices.choices)
    user = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
