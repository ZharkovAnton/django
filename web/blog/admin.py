from typing import Any

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from actions.models import LikeDislike

from .models import Article, Category, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ('author', 'content', 'user', 'parent')


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'status', 'author', 'short_title', 'total_likes')
    summernote_fields = ('content',)
    fields = ('category', 'title', 'status', 'author', 'image', 'content', 'tags', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    list_select_related = ('category', 'author')
    list_filter = ('status',)
    inlines = [
        CommentInline,
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        subquery_total_likes = (
            LikeDislike.objects.filter(
                content_type=ContentType.objects.get_for_model(Article), object_id=OuterRef('id')
            )
            .values('object_id')
            .annotate(total_likes=Sum('vote'))
            .values('total_likes')
        )
        queryset = queryset.annotate(
            total_likes=Coalesce(
                Subquery(subquery_total_likes),
                0,
            )
        )
        return queryset

    def total_likes(self, obj):
        return obj.total_likes


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'format_content', 'total_likes')

    # TODO: пернести в отдельный сервис
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        subquery_total_likes = (
            LikeDislike.objects.filter(
                content_type=ContentType.objects.get_for_model(Comment), object_id=OuterRef('id')
            )
            .values('object_id')
            .annotate(total_likes=Sum('vote'))
            .values('total_likes')
        )
        queryset = queryset.annotate(
            total_likes=Coalesce(
                Subquery(subquery_total_likes),
                0,
            )
        )
        return queryset

    def total_likes(self, obj):
        return obj.total_likes

    @admin.display
    def format_content(self):
        return format_html(self.content[:50])

