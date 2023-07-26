from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from actions.models import LikeDislike

from .serializers import LikeDislikeUpdateSerializer
from .services import LikeDislikeService


class VotesView(GenericAPIView):
    serializer_class = LikeDislikeUpdateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # [x]: перенес в сервис
        service = LikeDislikeService(serializer.validated_data, request.user)
        service.save_or_delete_like_dislike()

        sum_likes = service.get_sum_likes()

        return Response(
            {'detail': _('The like has been updated'), 'sum_likes': sum_likes},
            status=status.HTTP_200_OK,
        )
