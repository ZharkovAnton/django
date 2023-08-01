from typing import Any

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from actions.models import LikeDislike
from blog.models import Article

User = get_user_model()


class LikeDislikeInline(admin.TabularInline):
    model = LikeDislike
    readonly_fields = ('article_content', 'article_title', 'article_created')
    fields = ('article_title', 'article_content', 'article_created')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return (
            super()
            .get_queryset(request)
            .filter(content_type=ContentType.objects.get_for_model(Article))
            .prefetch_related('content_object')
            .all()
        )

    def article_content(self, obj):
        return obj.articles.first().content

    def article_title(self, obj):
        return obj.articles.first().title

    def article_created(self, obj):
        return obj.articles.first().created


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('-id',)
    list_display = ('email', 'full_name', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')

    fieldsets = (
        (_('Personal info'), {'fields': ('id', 'first_name', 'last_name', 'email', 'birthday', 'gender')}),
        (_('Secrets'), {'fields': ('password',)}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    readonly_fields = ('id',)
    inlines = [
        LikeDislikeInline,
    ]


title = settings.PROJECT_TITLE

admin.site.site_title = title
admin.site.site_header = title
admin.site.site_url = '/'
admin.site.index_title = title

admin.site.unregister(Group)
