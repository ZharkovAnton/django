from typing import Union

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.db.models.functions import Coalesce

from actions.models import LikeDislike
from blog.models import Article, Comment

from main.models import UserType


# TODO: !!! как избавиться от запроса в БД ContentType и проверить типизацию
class LikeDislikeService:
    def __init__(self, data: dict, user: UserType, *args, **kwargs) -> None:
        self.model_name: str = data['model']
        self.vote_type: str = data['vote_type']
        self.object_id: str = data['object_id']
        self.user = user

    def get_instance(self) -> Union[Article, Comment]:
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
