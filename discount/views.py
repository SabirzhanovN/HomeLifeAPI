from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from brand.permissions import IsAdminOrReadOnly

from .serializers import DiscountSerializer
from .models import Discount


class DiscountViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for the Discount model.
    It handles the creation, updating, and deletion of discounts, ensuring
    that the associated products have their discounted prices updated accordingly.

    * GET methods available for any user
    """
    serializer_class = DiscountSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Discount.objects.all()

    def perform_create(self, serializer):
        """
        Handle the creation of a new discount.
        This method updates the price_after_discount and discount_percent fields
        for all products associated with the newly created discount.
        """
        instance = serializer.save()
        for product in instance.products.all():
            product.price_after_discount = product.price - (product.price * instance.percent / 100)
            product.discount_percent = instance.percent
            product.save()

    def perform_update(self, serializer):
        """
        Handle the update of an existing discount.
        This method resets the price_after_discount and discount_percent fields for
        all products previously associated with the discount, and then updates these
        fields for the new set of associated products.
        """
        instance = serializer.instance

        old_products = set(instance.products.all())
        new_products = set(serializer.validated_data['products'])

        percent = int(serializer.validated_data['percent'])

        for product in old_products:
            product.price_after_discount = None
            product.discount_percent = 0
            product.save()
            print(f"Remove discount from {product.name}. price_after_discount -> {product.price_after_discount}")

        for product in new_products:
            product.price_after_discount = product.price - (product.price * percent / 100)
            product.discount_percent = percent
            product.save()
            print(f"Add discount to {product.name}. price_after_discount changed to {product.price_after_discount}")

        instance.products.set(new_products)
        instance.save()

        serializer.save()

    def perform_destroy(self, instance):
        """
        Handle the deletion of a discount.
        This method resets the price_after_discount and discount_percent fields for
        all products associated with the discount being deleted.
        """
        for product in instance.products.all():
            product.price_after_discount = None
            product.discount_percent = 0
            product.save()

        instance.delete()
