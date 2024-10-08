from rest_framework import serializers

from review.serializers import GradeDescriptionListSerializer
from .models import Catalog, Category, ProductType, Color, Product


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ('id', 'name')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'catalog')
        read_only_fields = ('id',)


class CatalogDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'categories')
        read_only_fields = ('id', 'name', 'categories')


class CategoryDetailSerializer(serializers.ModelSerializer):
    grade_descriptions = GradeDescriptionListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'catalog', 'grade_descriptions')
        read_only_fields = ('id', 'name', 'catalog', 'grade_descriptions')


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ('id', 'name', 'category')
        read_only_fields = ('id',)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name', 'color_code')
        read_only_fields = ('id',)


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'main_image',
                  'image_1', 'image_2', 'price',
                  'price_after_discount', 'grade')
        # fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id',)
