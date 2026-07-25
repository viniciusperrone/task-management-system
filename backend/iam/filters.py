from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model


User = get_user_model()


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='icontains')
    username = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['email', 'username', 'is_active']
