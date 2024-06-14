from rest_framework import serializers

from shop.models import Product


class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'main_image', 'price', 'price_after_discount')


class CartSerializer(serializers.Serializer):
    product = serializers.JSONField()
    quantity = serializers.IntegerField(required=False)
    override_quantity = serializers.BooleanField(required=False)
    remove = serializers.BooleanField(required=False)
    clear = serializers.BooleanField(required=False)
