from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db.models import Count, F
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.permissions import IsOwnerOrReadOnly
from api.v1.profile_app.serializers import (
    ProfileSerializer,
    ProfileUpdateAvatarSerializer,
    ProfileUpdateBIOSerializer,
    ProfileUpdatePasswordSerializer,
    UserListSerializer,
)
from api.v1.profile_app.services import ProfileUpdateService

if TYPE_CHECKING:
    from main.models import UserType

User: 'UserType' = get_user_model()


class ProfileDetailView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        queryset = User.objects.all().annotate(comments=Count('comment_set'), articles=Count('article_set'))
        print(str(queryset.query))
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        return  queryset.get(id=self.kwargs['user_id'])

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class ProfileUpdateBIOView(GenericAPIView):
    serializer_class = ProfileUpdateBIOSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def put(self, request):
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
    permission_classes = (IsOwnerOrReadOnly, )

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
    permission_classes = (IsOwnerOrReadOnly, )
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
    permission_classes = (AllowAny, )

    def get_queryset(self):
        return User.objects.all().order_by(F('is_active').desc(), F('date_joined').asc())

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
