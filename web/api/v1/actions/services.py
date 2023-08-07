from typing import Union

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, QuerySet
from django.db.models.functions import Coalesce
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from django.utils.translation import gettext_lazy as _

from actions.models import LikeDislike
from blog.models import Article, Comment

from main.models import UserType

User = get_user_model()



class LikeDislikeService:
    def __init__(self, data: dict, user: UserType) -> None:
        self.model_name: str = data['model']
        self.vote_type: str = data['vote_type']
        self.object_id: str = data['object_id']
        self.user = user

    def get_instance(self) -> Article | Comment:
        return apps.get_model(app_label='blog', model_name=self.model_name).objects.get(pk=self.object_id)

    def get_model(self) -> Union[Article, Comment]:
        return apps.get_model(app_label='blog', model_name=self.model_name)

    def save_or_delete_like_dislike(self) -> None:
        instance = self.get_instance()
        try:
            likedislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(instance), object_id=self.object_id, user=self.user
            )
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
            else:
                likedislike.delete()
        except LikeDislike.DoesNotExist:
            instance.votes.create(user=self.user, vote=self.vote_type)

    def get_sum_likes(self) -> int:
        return LikeDislike.objects.filter(
            content_type=ContentType.objects.get_for_model(self.get_instance()), object_id=self.get_instance().id
        ).aggregate(sum_likes=Coalesce(Sum('vote'), 0))['sum_likes']


class FollowerQueryService:
    def get_user(self, user_id: int) -> UserType:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            raise NotFound(_('Requested user does not exist')) from e

    def get_followers(self, user: UserType) -> QuerySet[UserType]:
        return user.followers.all()

    def get_following(self, user: UserType) -> QuerySet[UserType]:
        return user.following.all()
