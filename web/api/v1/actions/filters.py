from django.db.models import Q
from django_filters import rest_framework as filters


class FollowFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    first_name = filters.OrderingFilter(
        fields=(('first_name', 'first_name'),),
    )

    def search_filter(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))
