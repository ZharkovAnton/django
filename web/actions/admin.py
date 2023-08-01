from django.contrib import admin

from actions.models import Follower


# Register your models here.
@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    pass
