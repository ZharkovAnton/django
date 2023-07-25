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


class VotesView(GenericAPIView):
    serializer_class = LikeDislikeUpdateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO: перенести в сервис логику
        model = apps.get_model(app_label='blog', model_name=serializer.validated_data['model'])
        vote_type = serializer.validated_data['vote_type']
        obj = model.objects.get(pk=serializer.validated_data['object_id'])
        try:
            likedislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user
            )
            if likedislike.vote is not vote_type:
                likedislike.vote = vote_type
                likedislike.save(update_fields=['vote'])
            else:
                likedislike.delete()
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=vote_type)

        sum_likes = LikeDislike.objects.filter(
            content_type=ContentType.objects.get_for_model(obj), object_id=obj.id
        ).aggregate(sum_likes=Coalesce(Sum('vote'), 0))['sum_likes']
        print(sum_likes)

        return Response(
            {'detail': _('The like has been updated'), 'sum_likes': sum_likes},
            status=status.HTTP_200_OK,
        )
