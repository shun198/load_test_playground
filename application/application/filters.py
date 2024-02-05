import django_filters
from django.db.models import Q
from django.db.models.functions import Concat

from application.models import Customer


class CustomerFilter(django_filters.FilterSet):
    """お客様の
    - 氏名・カナ氏名
    - 住所

    で絞り込むFilter

    Args:
        django_filters
    """

    name = django_filters.CharFilter(method="search_name", label="name")

    class Meta:
        model = Customer
        fields = ["name"]

    def search_name(self, queryset, name, value):
        return queryset.filter(
            Q(name__contains=value) | Q(kana__contains=value)
        )

