from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.apps import apps

from actions.models import LikeDislike
from .serializers import LikeDislikeUpdateSerializer

def get_vote_type_by_name(type_name):
    if type_name == "LIKE":
        return LikeDislike.LIKE
    elif type_name == "DISLIKE":
        return LikeDislike.DISLIKE
    else:
        return None


class VotesView(GenericAPIView):
    serializer_class = LikeDislikeUpdateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        model = apps.get_model(app_label='blog', model_name=serializer.validated_data['model'])
        vote_type = get_vote_type_by_name(serializer.validated_data['vote_type'])
        obj = model.objects.get(pk=serializer.validated_data['article_id'])
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
            if likedislike.vote is not vote_type:
                likedislike.vote = vote_type
                likedislike.save(update_fields=['vote'])
            else:
                likedislike.delete()
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=vote_type)

        return Response(
            {'detail': _('The like has been updated')},
            status=status.HTTP_200_OK,
        )
