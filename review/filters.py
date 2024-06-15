import django_filters

from .models import Review
from shop.models import Product


class ReviewFilter(django_filters.FilterSet):
    product = django_filters.ModelChoiceFilter(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = {
            'product': ['exact']
        }
