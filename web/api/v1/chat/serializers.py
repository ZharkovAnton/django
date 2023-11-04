from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class UserChatListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'avatar', 'full_name')

    def get_avatar(self, obj):
        return obj.get_absolute_url_for_avatar()


class UserChatIdsListSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())
