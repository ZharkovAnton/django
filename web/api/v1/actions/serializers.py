from django.contrib.auth import get_user_model
from django.db.models import TextChoices
from rest_framework import serializers

from actions.models import Follower, LikeDislike

User = get_user_model()


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
