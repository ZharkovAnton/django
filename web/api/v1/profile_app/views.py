from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db.models import Count, F, OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from actions.models import LikeDislike
from api.v1.profile_app.serializers import (
    ProfileSerializer,
    ProfileUpdateAvatarSerializer,
    ProfileUpdateBIOSerializer,
    ProfileUpdatePasswordSerializer,
    UserListSerializer,
)
from api.v1.profile_app.services import ProfileUpdateService
from blog.models import Article, Comment
from src.celery import app
from celery.result import AsyncResult

if TYPE_CHECKING:
    from main.models import UserType

User: 'UserType' = get_user_model()


class ProfileDetailView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        count_comment_subquery = (
            Comment.objects.filter(user=OuterRef('id'))
            .values('author')
            .annotate(count_comments=Count('content'))
            .values('count_comments')
        )
        count_article_subquery = (
            Article.objects.filter(author=OuterRef('id'))
            .values('author')
            .annotate(count_article=Count('content'))
            .values('count_article')
        )
        total_likes = (
            LikeDislike.objects.filter(content_type=11, user=OuterRef('id'))
            .values('user')
            .annotate(total_likes=Sum('vote'))
            .values('total_likes')
        )

        count_followers = (
            User.objects.filter(following=OuterRef('id'))
            .values('following')
            .annotate(count_followers=Count('email'))
            .values('count_followers')
        )

        return User.objects.annotate(
            count_articles=Coalesce(Subquery(count_article_subquery), 0),
            count_comments=Coalesce(Subquery(count_comment_subquery), 0),
            total_likes=Coalesce(Subquery(total_likes), 0),
            count_followers=Coalesce(Subquery(count_followers), 0),
        )

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.get(id=self.kwargs['user_id'])

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class ProfileUpdateBIOView(GenericAPIView):
    serializer_class = ProfileUpdateBIOSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = ProfileUpdateService()
        service.update_user(request.user, serializer.validated_data)

        return Response(
            {'detail': _('The profile has been updated')},
            status=status.HTTP_200_OK,
        )


class ProfileUpdatePasswordView(GenericAPIView):
    serializer_class = ProfileUpdatePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = ProfileUpdateService()
        service.update_password(request.user, request.data)

        return Response(
            {'detail': _('The password has been updated')},
            status=status.HTTP_200_OK,
        )


class ProfileUpdateAvatarView(GenericAPIView):
    serializer_class = ProfileUpdateAvatarSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = ProfileUpdateService()
        service.update_avatar(request.user, serializer.validated_data['avatar'])

        return Response(
            {'detail': _('The avatar has been updated')},
            status=status.HTTP_200_OK,
        )


class UsersListView(GenericAPIView):
    serializer_class = UserListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return User.objects.all().order_by(F('is_active').desc(), F('date_joined').asc())

    def get(self, request, *args, **kwargs):
        res: AsyncResult = app.send_task('tasks.add', args=[1,2], queue='project_1')
        while res.ready() is False:
            print(res.ready())
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
