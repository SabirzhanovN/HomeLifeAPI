import django_filters

from brand.models import Brand
from .models import Product, ProductType, Category


class ProductTypeFilter(django_filters.FilterSet):
    """
    The ProductTypeFilter class provides filtering functionality for the ProductType.
    Filtering can be done by the following fields:
    - category (multiple values represented by foreign keys)

    * Example of URL
    /api/shop/product-type/?category=1&category=3
    """
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = ProductType
        fields = {
            'category': ['exact']
        }


class ProductFilter(django_filters.FilterSet):
    """
    The ProductFilter class provides filtering functionality for the Product.
    Filtering can be done by the following fields:
    - price (price range, set through two separate filters: price_min and price_max)
    - brand (multiple values represented by foreign keys)
    - type (multiple values represented by foreign keys)
    - Power (range of power values, set through two separate filters: power_min and power_max)

    * Example of URL
    /api/shop/product/?brand=1&brand=2&type=1&type=2&power_min=100&power_max=200&price_min=50&price_max=500
    """
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all())
    type = django_filters.ModelMultipleChoiceFilter(queryset=ProductType.objects.all())
    power_min = django_filters.NumberFilter(field_name="power", lookup_expr='gte')
    power_max = django_filters.NumberFilter(field_name="power", lookup_expr='lte')

    class Meta:
        model = Product
        fields = {
            'price': ['exact', 'gte', 'lte'],
            'brand': ['exact'],
            'type': ['exact'],
            'power': ['exact', 'gte', 'lte'],
        }
