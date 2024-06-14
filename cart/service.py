from decimal import Decimal

from django.conf import settings

from shop.models import Product
from .serializers import ProductCartSerializer


class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add product to the cart or update its quantity
        """
        try:
            product_id = str(product["id"])
        except Exception as e:
            print(e)
            raise IndexError

        if product_id not in self.cart:
            try:
                product_obj = Product.objects.get(id=product_id)
            except Exception as e:
                print(e)
                raise ValueError

            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product_obj.price_after_discount if product_obj.price_after_discount else product_obj.price)
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart
        """
        try:
            product_id = str(product["id"])
        except Exception as e:
            print(e)
            raise IndexError

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Loop through cart items and fetch the products from the database
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = ProductCartSerializer(product).data
        for item in cart.values():
            product = Product.objects.get(id=item['product']['id'])
            price_obj = product.price_after_discount if product.price_after_discount else product.price
            item["price"] = Decimal(price_obj)
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
