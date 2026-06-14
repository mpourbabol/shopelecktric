import django_filters
from django.utils.translation import gettext_lazy as _

from .models import Brand, Category, Product


class ProductFilter(django_filters.FilterSet):
    brand = django_filters.ModelChoiceFilter(
        queryset=Brand.objects.all(),
        label=_('Brand'),
    )
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.filter(sub_cat=False),
        label=_('Category'),
    )
    min_price = django_filters.NumberFilter(
        field_name='unit_price',
        lookup_expr='gte',
        label=_('Min price'),
    )
    max_price = django_filters.NumberFilter(
        field_name='unit_price',
        lookup_expr='lte',
        label=_('Max price'),
    )

    class Meta:
        model = Product
        fields = ['brand', 'category', 'min_price', 'max_price']
