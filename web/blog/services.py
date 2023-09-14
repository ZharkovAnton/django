from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Sum
from django.db.models.query import QuerySet

from actions.models import LikeDislike

from .models import Article, Comment


class AdminQueryService:
    def get_total_likes_for_comment(self) -> QuerySet[LikeDislike]:
        return (
            LikeDislike.objects.filter(
                content_type=ContentType.objects.get_for_model(Comment), object_id=OuterRef('id')
            )
            .values('object_id')
            .annotate(total_likes=Sum('vote'))
            .values('total_likes')
        )

    def get_total_likes_for_article(self) -> QuerySet[LikeDislike]:
        return (
            LikeDislike.objects.filter(
                content_type=ContentType.objects.get_for_model(Article), object_id=OuterRef('id')
            )
            .values('object_id')
            .annotate(total_likes=Sum('vote'))
            .values('total_likes')
        )
