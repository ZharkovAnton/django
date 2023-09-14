from typing import Any

from django.contrib import admin
from django.db.models import Subquery
from django.db.models.functions import Coalesce
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from .models import Article, Category, Comment
from .services import AdminQueryService


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

    # [x]: ?
    def get_queryset(self, request):
        service = AdminQueryService()

        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_likes=Coalesce(
                Subquery(service.get_total_likes_for_article()),
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

    # [x]: ?
    def get_queryset(self, request):
        service = AdminQueryService()

        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_likes=Coalesce(
                Subquery(service.get_total_likes_for_comment()),
                0,
            )
        )

        return queryset

    def total_likes(self, obj):
        return obj.total_likes

    @admin.display
    def format_content(self, obj):
        return format_html(obj.content[:50])
