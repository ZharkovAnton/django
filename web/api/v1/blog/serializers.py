from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from taggit.models import Tag

from blog.models import Article, Category, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'author', 'content', 'updated')


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

    class Meta:
        model = Article
        fields = ('title', 'url', 'author', 'category', 'created', 'updated', 'comments_count', 'image')


class FullArticleSerializer(TaggitSerializer, ArticleSerializer):
    comments = CommentSerializer(source='comment_set', many=True)
    tags = TagListSerializerField()

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + (
            'content',
            'comments',
            'tags'
        )


class ArticleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    class Meta:
        model = Article
        fields = ('title', 'category', 'content', 'image')


class TagListSerializer(serializers.Serializer):
    name = serializers.CharField()
