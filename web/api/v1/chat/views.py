from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import serializers


User: 'UserType' = get_user_model()

if TYPE_CHECKING:
    from main.models import UserType

class UserChatListView(GenericAPIView):
    serializer_class = serializers.UserChatIdsListSerializer
    # TODO: ??? как здесь не получать ошибку что пользователь не авторизован
    permission_classes = ()

    def get_queryset(self):
        # TODO: !!! user_ids можно здесь создать?
        user_ids = self.request.GET.getlist('user_id')
        return User.objects.filter(id__in=user_ids)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_users = serializers.UserChatListSerializer(queryset, many=True)
        print('HERE', serializer_users.data)

        return Response(serializer_users.data)
