from django.contrib.auth import get_user_model
from rest_framework import serializers
from actions.models import LikeDislike


User = get_user_model()

class LikeDislikeUpdateSerializer(serializers.Serializer):
    model = serializers.CharField()
    vote_type = serializers.CharField()
    article_id = serializers.IntegerField()


class LikeDislikeFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ('user', 'vote')
