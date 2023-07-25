from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TaggitSerializer, TagListSerializerField

from api.v1.actions.serializers import LikeDislikeFullSerializer
from blog.models import Article, Category, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    children = serializers.SerializerMethodField()
    votes = LikeDislikeFullSerializer(many=True)
    count_like = serializers.IntegerField()

    def get_children(self, comment):
        children_comments = comment.children.all()
        serializer = CommentSerializer(instance=children_comments, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'updated', 'children', 'count_like', 'votes')


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    author = UserSerializer()
    category = CategorySerializer()
    comments_count = serializers.IntegerField()
    count_like_dislike = serializers.IntegerField()
    votes = LikeDislikeFullSerializer(many=True)

    class Meta:
        model = Article
        fields = (
            'title',
            'url',
            'author',
            'category',
            'created',
            'updated',
            'comments_count',
            'image',
            'id',
            'count_like_dislike',
            'votes',
        )


class FullArticleSerializer(TaggitSerializer, ArticleSerializer):
    tags = TagListSerializerField()

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ('content', 'tags')


class ArticleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        model = Article
        fields = ('title', 'category', 'content', 'image')


class TagListSerializer(serializers.Serializer):
    name = serializers.CharField()


class CommentCreateSerializer(serializers.ModelSerializer):
    article = serializers.SlugRelatedField(queryset=Article.objects.all(), slug_field='slug')
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), allow_null=True)

    class Meta:
        model = Comment
        fields = ('content', 'article', 'parent')
