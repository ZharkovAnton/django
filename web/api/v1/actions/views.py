from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .filters import FollowFilter
from .serializers import FollowersSerializer, FollowersUpdateDeleteSerializer, LikeDislikeUpdateSerializer
from .services import LikeDislikeService
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


class FollowerViewSet(viewsets.GenericViewSet):
    serializer_class = FollowersSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FollowFilter
    pagination_class = BasePageNumberPagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        if self.action == 'following':
            return user.following.all()
        elif self.action == 'followers':
            return user.followers.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        filtered_queryset = self.filterset_class(self.request.GET, queryset=queryset).qs
        paginated_queryset = paginator.paginate_queryset(filtered_queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def following(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def followers(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
