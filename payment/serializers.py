from rest_framework import serializers

from cart.service import Cart
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'total_price', 'products', 'status')

    def create(self, validated_data):
        """
        Overriding the create method to include cart data from the session.

        This method extracts the cart data from the user's session and sets
        the 'products' and 'total_price' fields in the order being created.

        Args:
            validated_data (dict): The validated data for creating the order.

        Returns:
            Order: The created Order instance.

        Raises:
            serializers.ValidationError: If the cart is empty or not found in the session.
        """
        request = self.context.get('request')
        cart = request.session.get('cart', {})

        if not cart:
            raise serializers.ValidationError("Cart is empty")

        products = cart
        total_price = Cart(request).get_total_price()

        validated_data['products'] = products
        validated_data['total_price'] = total_price

        return super().create(validated_data)

