from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from actions.models import EventAction

from .filters import FollowFilter
from .serializers import (
    EventSerializer,
    FollowersSerializer,
    FollowersUpdateDeleteSerializer,
    LikeDislikeUpdateSerializer,
)
from .services import FollowerQueryService, LikeDislikeService
from main.pagination import BasePageNumberPagination

User = get_user_model()


class VotesView(GenericAPIView):
    serializer_class = LikeDislikeUpdateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = LikeDislikeService(serializer.validated_data, request.user)
        service.save_or_delete_like_dislike()

        sum_likes = service.get_sum_likes()

        return Response(
            {'detail': _('The like has been updated'), 'sum_likes': sum_likes},
            status=status.HTTP_200_OK,
        )


class FollowerUpdateDeleteView(GenericAPIView):
    serializer_class = FollowersUpdateDeleteSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_user = User.objects.get(id=serializer.validated_data['id'])
        try:
            to_user.followers.get(id=request.user.id)
            to_user.followers.remove(request.user.id)
        except User.DoesNotExist:
            to_user.followers.add(request.user.id)

        count_followers = to_user.followers.count()

        return Response(
            {'detail': _('The followers has been updated'), 'count_followers': count_followers},
            status=status.HTTP_200_OK,
        )


class FollowerViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FollowersSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FollowFilter
    pagination_class = BasePageNumberPagination

    def get_queryset(self):
        service = FollowerQueryService()

        if self.action == 'following_by_id':
            user = service.get_user(self.kwargs['user_id'])
            return service.get_following(user)
        elif self.action == 'followers_by_id':
            user = service.get_user(self.kwargs['user_id'])
            return service.get_followers(user)
        elif self.action == 'following_current_user':
            return service.get_following(self.request.user)
        elif self.action == 'followers_current_user':
            return service.get_followers(self.request.user)

    def following_by_id(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def followers_by_id(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def following_current_user(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def followers_current_user(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EventView(GenericAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return EventAction.objects.all().order_by('-created')

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
