from django.contrib.auth import get_user_model
from django.db.models import TextChoices
from rest_framework import serializers

from actions.models import EventAction, LikeDislike

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name')


class LikeDislikeModelChoice(TextChoices):
    ARTICLE = 'Article'
    COMMENT = 'Comment'


class LikeDislikeUpdateSerializer(serializers.Serializer):
    model = serializers.ChoiceField(choices=LikeDislikeModelChoice.choices)
    vote_type = serializers.ChoiceField(choices=LikeDislike.Vote.choices)
    object_id = serializers.IntegerField(min_value=1)


class LikeDislikeFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ('user', 'vote')


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'avatar', 'email', 'followers')


class FollowersUpdateDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)

class EventSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    name = serializers.CharField(source='get_name_display')

    class Meta:
        model = EventAction
        fields = ('user', 'name', 'created')
